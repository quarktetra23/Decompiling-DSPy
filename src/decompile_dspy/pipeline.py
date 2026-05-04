import json
import re
import dspy

from .prompts import (
    R_REF_PROMPT,
    PROMPT_SIMPLIFY,
    PROMPT_RENAME,
    PROMPT_COMMENT,
    REFINE_TO_COMPILABLE,
)
from .compile_check import gcc_syntax_check


def _fill_prompt(template: str, code: str) -> str:
    return template.replace("{code}", code)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()


def _parse_yes_no_triplet(text: str) -> tuple[bool, bool, bool]:
    toks = re.findall(r"\b(yes|no)\b", text.lower())
    toks = toks[:3] + ["no"] * max(0, 3 - len(toks))

    return (
        toks[0] == "yes",
        toks[1] == "yes",
        toks[2] == "yes",
    )


def _safe_json_map(text: str) -> dict[str, str]:
    try:
        text = _strip_code_fences(text)

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        obj = json.loads(text)

        if not isinstance(obj, dict):
            return {}

        return {
            str(k).strip(): str(v).strip()
            for k, v in obj.items()
            if str(k).strip() and str(v).strip()
        }

    except Exception:
        return {}


# ------------------------------------------------------------
# C CODE STRUCTURE HELPERS
# ------------------------------------------------------------

def _extract_function_names(code: str) -> list[str]:
    pattern = (
        r"^\s*"
        r"(?:[A-Za-z_][\w\s\*\d]*?)"
        r"\s+"
        r"([A-Za-z_]\w*)"
        r"\s*\([^;]*\)"
        r"\s*\{"
    )

    return re.findall(pattern, code, flags=re.MULTILINE)


def _has_duplicate_code(code: str) -> bool:
    cleaned = re.sub(r"\s+", "", code)

    if len(cleaned) < 80:
        return False

    midpoint = len(cleaned) // 2
    left = cleaned[:midpoint]
    right = cleaned[midpoint:]

    if left and left == right:
        return True

    main_like_count = len(re.findall(r"\b_main\s*\(", code))
    if main_like_count > 2:
        return True

    return False


def _added_forbidden_wrapper(original: str, candidate: str) -> bool:
    original_funcs = set(_extract_function_names(original))
    candidate_funcs = set(_extract_function_names(candidate))

    # Do not add a new main if the input only had _main.
    if "main" not in original_funcs and "main" in candidate_funcs:
        return True

    # Do not add printing/logging.
    if "printf" in candidate and "printf" not in original:
        return True

    # Be strict about new includes.
    if "#include" in candidate and "#include" not in original:
        return True

    # Do not add multiple new functions.
    if len(candidate_funcs) > len(original_funcs) + 1:
        return True

    return False


def _call_sequence(code: str) -> list[str]:
    names = re.findall(r"\b([A-Za-z_]\w*)\s*\(", code)

    keywords = {
        "if",
        "for",
        "while",
        "switch",
        "return",
        "sizeof",
        "int",
        "char",
        "long",
        "short",
        "float",
        "double",
        "void",
        "unsigned",
        "signed",
    }

    return [name for name in names if name not in keywords]


def _removed_important_calls(original: str, candidate: str) -> bool:
    original_calls = _call_sequence(original)
    candidate_calls = _call_sequence(candidate)

    protected = []

    for name in original_calls:
        if name.startswith("_"):
            protected.append(name)
        elif name in {"printf", "strcpy", "strcmp", "strlen", "malloc", "free"}:
            protected.append(name)

    for name in protected:
        if name not in candidate_calls:
            return True

    return False


def _sanitize_candidate(original: str, candidate: str) -> str:
    candidate = _strip_code_fences(candidate)

    # Remove accidental duplicated full output if it is exactly doubled.
    half = len(candidate) // 2
    left = candidate[:half].strip()
    right = candidate[half:].strip()

    if left and left == right:
        candidate = left

    return candidate.strip()


def _is_candidate_safe(original: str, candidate: str) -> tuple[bool, str]:
    candidate = _sanitize_candidate(original, candidate)

    if not candidate:
        return False, "empty candidate"

    if _has_duplicate_code(candidate):
        return False, "candidate appears duplicated"

    if _added_forbidden_wrapper(original, candidate):
        return False, "candidate added wrapper, header, printf, or extra function"

    if _removed_important_calls(original, candidate):
        return False, "candidate removed important function call"

    original_funcs = _extract_function_names(original)
    candidate_funcs = _extract_function_names(candidate)

    if original_funcs and candidate_funcs:
        if original_funcs[0] != candidate_funcs[0]:
            return False, "candidate changed primary function name"

    return True, ""


# ------------------------------------------------------------
# RENAME SAFETY
# ------------------------------------------------------------

def _bad_new_name(new: str) -> bool:
    risky_words = {
        "request",
        "response",
        "user",
        "token",
        "admin",
        "role",
        "path",
        "body",
        "password",
        "database",
        "socket",
        "file",
        "client",
        "server",
        "price",
        "method",
    }

    lowered = new.lower()

    return any(word in lowered for word in risky_words)


def _declared_local_names(code: str) -> set[str]:
    names = set()

    # Examples:
    # unsigned int v0;
    # char *v2;
    # long long result;
    declaration_pattern = (
        r"\b"
        r"(?:unsigned\s+|signed\s+)?"
        r"(?:int|char|long|short|float|double|uint128_t)"
        r"(?:\s+long)?"
        r"\s+"
        r"(?:\*+\s*)?"
        r"([A-Za-z_]\w*)"
        r"\b"
    )

    for name in re.findall(declaration_pattern, code):
        names.add(name)

    return names


def _apply_rename_map(code: str, mapping: dict[str, str]) -> str:
    safe_mapping: dict[str, str] = {}
    declared_names = _declared_local_names(code)

    for old, new in mapping.items():
        if not old or not new or old == new:
            continue

        if not re.match(r"^[A-Za-z_]\w*$", old):
            continue

        if not re.match(r"^[A-Za-z_]\w*$", new):
            continue

        # Only rename local-looking variables.
        if old not in declared_names and not re.match(r"^v\d+$|^flag$|^cur$|^i$|^j$", old):
            continue

        # Avoid business-meaning hallucinations.
        if _bad_new_name(new):
            continue

        # Do not rename functions.
        if re.search(rf"\b{re.escape(old)}\s*\(", code):
            continue

        safe_mapping[old] = new

    for old, new in safe_mapping.items():
        code = re.sub(rf"\b{re.escape(old)}\b", new, code)

    return code


# ------------------------------------------------------------
# DSPy MODULES
# ------------------------------------------------------------

class Referee(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("code -> decision")

    def forward(self, code: str):
        prompt = _fill_prompt(R_REF_PROMPT, code)
        out = self.predict(code=prompt)

        need_simplify, need_comment, need_rename = _parse_yes_no_triplet(out.decision)

        return dspy.Prediction(
            need_simplify=need_simplify,
            need_comment=need_comment,
            need_rename=need_rename,
        )


class Advisor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("prompt -> out")

    def forward(self, prompt: str):
        out = self.predict(prompt=prompt)
        return dspy.Prediction(text=_strip_code_fences(out.out))


class Operator:
    def accept(self, c_code: str) -> tuple[bool, str]:
        return gcc_syntax_check(c_code)


# ------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------

class DecompileRefinePipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.referee = Referee()
        self.advisor = Advisor()
        self.operator = Operator()

    def _initial_refine(self, angr_code: str) -> str:
        prompt = _fill_prompt(REFINE_TO_COMPILABLE, angr_code)
        return self.advisor(prompt).text

    def _try_accept(self, original: str, candidate: str) -> tuple[bool, str, str]:
        candidate = _sanitize_candidate(original, candidate)

        safe, reason = _is_candidate_safe(original, candidate)

        if not safe:
            return False, candidate, reason

        ok, compile_msg = self.operator.accept(candidate)

        if not ok:
            return False, candidate, compile_msg

        return True, candidate, ""

    def forward(self, angr_code: str):
        notes: dict = {
            "applied": [],
        }

        # ----------------------------------------------------
        # Step 1: Initial conservative cleanup
        # ----------------------------------------------------
        candidate = self._initial_refine(angr_code)
        ok, refined, msg = self._try_accept(angr_code, candidate)

        notes["initial_compile_ok"] = ok
        notes["initial_compile_msg"] = msg

        if not ok:
            refined = angr_code
            notes["fallback"] = "angr_used_after_initial_reject"

        # ----------------------------------------------------
        # Step 2: Referee decides which transformations to try
        # ----------------------------------------------------
        decision = self.referee(refined)

        steps = []

        if decision.need_simplify:
            steps.append("simplify")

        if decision.need_rename:
            steps.append("rename")

        if decision.need_comment:
            steps.append("comment")

        # Keep transformations ordered and predictable.
        order = [
            step for step in ["simplify", "rename", "comment"]
            if step in steps
        ]

        current = refined

        # ----------------------------------------------------
        # Step 3: Apply selected transformations with guards
        # ----------------------------------------------------
        for step in order:
            if step == "simplify":
                prompt = _fill_prompt(PROMPT_SIMPLIFY, current)
                raw_candidate = self.advisor(prompt).text

            elif step == "rename":
                prompt = _fill_prompt(PROMPT_RENAME, current)
                mapping_text = self.advisor(prompt).text
                mapping = _safe_json_map(mapping_text)

                notes["rename_map_raw"] = mapping

                raw_candidate = _apply_rename_map(current, mapping)

            elif step == "comment":
                prompt = _fill_prompt(PROMPT_COMMENT, current)
                raw_candidate = self.advisor(prompt).text

            else:
                continue

            ok2, checked_candidate, msg2 = self._try_accept(current, raw_candidate)

            if ok2:
                current = checked_candidate
                notes["applied"].append(
                    {
                        "step": step,
                        "accepted": True,
                    }
                )
            else:
                notes["applied"].append(
                    {
                        "step": step,
                        "accepted": False,
                        "why": msg2[:300],
                    }
                )

        return dspy.Prediction(
            final_c=current,
            debug=notes,
        )
    






















    