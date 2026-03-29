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

def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()



def _parse_yes_no_triplet(text: str) -> tuple[bool, bool, bool]:
    toks = re.findall(r"\b(yes|no)\b", text.lower())
    toks = toks[:3] + ["no"] * max(0, 3 - len(toks))
    return (toks[0] == "yes", toks[1] == "yes", toks[2] == "yes")


def _safe_json_map(text: str) -> dict[str, str]:
    try:
        text2 = text.strip()

        if text2.startswith("{") and "'" in text2 and '"' not in text2:
            text2 = text2.replace("'", '"')

        obj = json.loads(text2)
        return {str(k): str(v) for k, v in obj.items()} if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _apply_rename_map(code: str, mapping: dict[str, str]) -> str:
    for old, new in mapping.items():
        if not old or not new or old == new:
            continue
        code = re.sub(rf"\b{re.escape(old)}\b", new, code)
    return code


def _normalize_main_signature(code: str) -> str:
    code = re.sub(r'\bunsigned\s+long\s+long\s+_main\s*\(\s*void\s*\)', 'int main(void)', code)
    code = re.sub(r'\bunsigned\s+int\s+_main\s*\(\s*void\s*\)', 'int main(void)', code)
    code = re.sub(r'\bint\s+_main\s*\(\s*void\s*\)', 'int main(void)', code)
    return code

class Referee(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("code -> decision")

    def forward(self, code: str):
        out = self.predict(code=R_REF_PROMPT.format(code=code))
        simp, comm, ren = _parse_yes_no_triplet(out.decision)
        return dspy.Prediction(
            need_simplify=simp,
            need_comment=comm,
            need_rename=ren
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

class DecompileRefinePipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.referee = Referee()
        self.advisor = Advisor()
        self.operator = Operator()

    def _initial_refine(self, angr_code: str):
        return self.advisor(
            REFINE_TO_COMPILABLE.format(code=angr_code)
        ).text

    def forward(self, angr_code: str):
        notes: dict = {"applied": []}
        refined = self._initial_refine(angr_code)
        ok, compile_msg = self.operator.accept(refined)

        notes["initial_compile_ok"] = ok
        notes["initial_compile_msg"] = compile_msg

        # Retry once if it fails
        if not ok:
            retry = self._initial_refine(refined)
            ok2, msg2 = self.operator.accept(retry)

            notes["retry_compile_ok"] = ok2
            notes["retry_compile_msg"] = msg2

            if ok2:
                refined = retry
                ok = True
            else:
                # fallback to original angr (safe baseline)
                refined = angr_code
                notes["fallback"] = "angr_used"

        dec = self.referee(refined)

        steps = []
        if dec.need_simplify: steps.append("simplify")
        if dec.need_comment: steps.append("comment")
        if dec.need_rename: steps.append("rename")

        order = [s for s in ["simplify", "comment", "rename"] if s in steps]

        current = refined

        for step in order:
            if step == "simplify":
                candidate = self.advisor(
                    PROMPT_SIMPLIFY.format(code=current)
                ).text

            elif step == "comment":
                candidate = self.advisor(
                    PROMPT_COMMENT.format(code=current)
                ).text

            else:  # rename
                mapping_text = self.advisor(
                    PROMPT_RENAME.format(code=current)
                ).text

                mapping = _safe_json_map(mapping_text)
                candidate = _apply_rename_map(current, mapping)

            ok2, msg2 = self.operator.accept(candidate)

            if ok2:
                current = candidate
                notes["applied"].append({"step": step, "accepted": True})
            else:
                notes["applied"].append({
                    "step": step,
                    "accepted": False,
                    "why": msg2[:300]
                })

        return dspy.Prediction(final_c=current, debug=notes)
    


