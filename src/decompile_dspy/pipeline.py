
import json
import re
import dspy
from dspy import load
from src.decompile_dspy.dspy_module import Decompiler

from .prompts import (
    R_REF_PROMPT,
    PROMPT_SIMPLIFY,
    PROMPT_RENAME,
    PROMPT_COMMENT,
    REFINE_TO_COMPILABLE,
)
from .compile_check import gcc_syntax_check

compiled = load("compiled_dspy.json")


def _parse_yes_no_triplet(text: str) -> tuple[bool, bool, bool]:
    toks = re.findall(r"\b(yes|no)\b", text.lower())
    toks = toks[:3] + ["no"] * max(0, 3 - len(toks))
    return (toks[0] == "yes", toks[1] == "yes", toks[2] == "yes")


def _safe_json_map(text: str) -> dict[str, str]:
    # Accept either {'a':'b'} or {"a":"b"}.
    # If it fails, return empty mapping.
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


class Referee(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("code -> decision")

    def forward(self, code: str):
        out = self.predict(code=R_REF_PROMPT.format(code=code))
        simp, comm, ren = _parse_yes_no_triplet(out.decision)
        return dspy.Prediction(need_simplify=simp, need_comment=comm, need_rename=ren)


class Advisor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("prompt -> out")

    def forward(self, prompt: str):
        out = self.predict(prompt=prompt)
        return dspy.Prediction(text=out.out)


class Operator:
    def accept(self, c_code: str) -> tuple[bool, str]:
        ok, msg = gcc_syntax_check(c_code)
        return ok, msg


class DecompileRefinePipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.referee = Referee()
        self.advisor = Advisor()
        self.operator = Operator()

    def forward(self, input_code: str):
        # Use compiled model instead of old GPT call
        result = compiled(assembly=input_code)
        clean_code = result.code

        # The rest of the pipeline can proceed as before, using clean_code
        ok, compile_msg = self.operator.accept(clean_code)
        if not ok:
            clean_code = input_code

        # Step 1: decide which smaller optimizations are needed (DeGPT’s R_ref)
        dec = self.referee(clean_code)
        steps = []
        if dec.need_simplify: steps.append("simplify")
        if dec.need_comment: steps.append("comment")
        if dec.need_rename: steps.append("rename")

        # Step 2: apply in an order that tends to help later steps
        order = [s for s in ["simplify", "comment", "rename"] if s in steps]

        current = clean_code
        notes = {"initial_compile_ok": ok, "initial_compile_msg": compile_msg, "applied": []}

        for step in order:
            if step == "simplify":
                candidate = self.advisor(PROMPT_SIMPLIFY.format(code=current)).text
            elif step == "comment":
                candidate = self.advisor(PROMPT_COMMENT.format(code=current)).text
            else:  # rename
                mapping_text = self.advisor(PROMPT_RENAME.format(code=current)).text
                mapping = _safe_json_map(mapping_text)
                candidate = _apply_rename_map(current, mapping)

            ok2, msg2 = self.operator.accept(candidate)
            if ok2:
                current = candidate
                notes["applied"].append({"step": step, "accepted": True})
            else:
                notes["applied"].append({"step": step, "accepted": False, "why": msg2[:500]})

        return dspy.Prediction(final_c=current, debug=notes)
