R_REF_PROMPT = """
You are reviewing decompiler-generated C-like code.

Decide whether the code needs each of the following, in this exact order:
1. structure simplification
2. comment appending
3. variable renaming

Answer with exactly three words: yes or no, in order.
No explanation.

Important:
- Say yes to simplification only if there are obvious redundant temporaries, dead variables, duplicated returns, numeric character constants, or awkward decompiler artifacts.
- Say yes to renaming only if variable purpose is directly proven by assignments, comparisons, loop use, pointer arithmetic, or function-call position.
- Say no to renaming if names would require guessing business meaning such as request, response, user, token, role, admin, file, socket, password, etc.
- Say yes to comments only for non-obvious loops, parser logic, bit manipulation, pointer arithmetic, or state machines.

Code:
{code}
"""


REFINE_TO_COMPILABLE = """
You are cleaning decompiler-generated C-like code.

Your task is conservative cleanup, not rewriting.

Priorities:
1. Preserve exact behavior.
2. Preserve function boundaries.
3. Preserve argument order and pointer/data flow.
4. Produce valid C.
5. Improve readability only when safe.

Hard rules:
- Output only C code.
- No markdown fences.
- No explanation.
- Do NOT duplicate the code.
- Do NOT add a new main function.
- Do NOT add printf, logging, test harnesses, or wrappers.
- Do NOT add new behavior.
- Do NOT add #include lines unless the input already had them or compilation absolutely requires them.
- Do NOT rename function names.
- Do NOT reorder function arguments.
- Do NOT swap source and destination buffers.
- Do NOT infer business roles from string contents alone.
- Do NOT rename stack buffers to request/response/user/token unless the data flow proves that role.
- Preserve calls exactly unless only syntax needs repair.
- Preserve all existing function calls.
- Preserve return values.
- Keep the same number of top-level functions as the input whenever possible.
- If the input has only _main, output only _main.
- If the input calls unknown external functions, keep their names and call sites unchanged.
- If decompiler intrinsics such as ___strcpy_chk appear, you may replace them with equivalent standard C calls only if argument meaning is clear.
- If uncertain, leave the code closer to the input.

Code:
{code}
"""


PROMPT_SIMPLIFY = """
You are simplifying decompiler-generated C code.

Goal:
Improve structure only when the transformation is directly supported by the code.

Allowed simplifications:
- Remove dead variables that are assigned but never used.
- Remove redundant copies such as temp = x; y = temp; when clearly safe.
- Replace numeric ASCII constants with character literals, such as 80 with 'P', only inside character comparisons.
- Replace repeated assignment-then-return patterns with direct returns only when behavior is identical.
- Simplify obvious if/else return patterns.
- Simplify state variables only when every transition is obvious and no path is lost.
- Keep function calls inside loops if they were inside loops.
- Keep pointer argument order exactly the same.

Forbidden transformations:
- Do NOT add headers.
- Do NOT add main.
- Do NOT add printf.
- Do NOT create wrappers.
- Do NOT invent helper functions.
- Do NOT remove function calls.
- Do NOT move function calls outside loops.
- Do NOT reorder arguments.
- Do NOT swap input/output buffers.
- Do NOT change constants unless the replacement is exactly equivalent.
- Do NOT precompute whole programs into constants.
- Do NOT simplify if the result requires guessing.

Output only valid C code.
No explanation.
No markdown fences.

Code:
{code}
"""


PROMPT_RENAME = """
You are renaming variables in decompiler-generated C code.

Goal:
Improve readability without changing behavior or inventing meaning.

Return only a JSON object mapping old local variable names to new local variable names.

Safe examples:
- loop index variables may become i, j, index if used as array/string indexes.
- accumulator variables may become total, sum, count, score if directly accumulated.
- variables used in byte masks may become low_byte, masked_value, shifted_value.
- variables used in ASCII/string scanning may become index, cursor, match_count.
- variables storing return values may become result.

Unsafe examples:
- Do NOT rename buffers to request or response unless function argument flow proves it.
- Do NOT rename values to user, token, admin, role, path, body, price, count, password, file, socket, database, etc. from string contents alone.
- Do NOT rename if there are multiple possible meanings.
- Do NOT rename function names.
- Do NOT rename struct fields.
- Do NOT invent new variables.
- Do NOT change pointer levels.
- Do NOT rename one variable based only on comments.
- Prefer no rename over risky rename.

Very important:
- If a buffer is filled with method/path/body/token-like strings but then passed as the first argument to a routing function, you may call it input_buffer or arg0_buffer, not request unless the function signature proves it.
- If a buffer is passed as the second argument and later scored, you may call it output_buffer only if the data flow proves it.
- Never swap roles.

Return only JSON.
If no safe renames exist, return {}.

Code:
{code}
"""


PROMPT_COMMENT = """
Add concise comments to decompiler-generated C code only when they clarify non-obvious logic.

Rules:
- Do NOT change code.
- Do NOT add headers.
- Do NOT add main.
- Do NOT add wrappers.
- Do NOT add speculative comments.
- Do NOT claim business meaning unless directly proven.
- Good comments explain:
  - state-machine transitions
  - pointer arithmetic
  - ASCII character comparisons
  - bit masking/shifting
  - loop invariants
  - call placement inside loops
- Bad comments guess application meaning.

Output only valid C code.
No explanation.
No markdown fences.

Code:
{code}
"""


