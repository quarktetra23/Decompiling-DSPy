R_REF_PROMPT = """
You are reviewing decompiler-generated C-like code.

Decide whether the code needs each of the following, in this exact order:
1. structure simplification
2. comment appending
3. variable renaming

Answer with exactly three words: yes or no, in order.
No explanation.

Code:
{code}
"""


PROMPT_SIMPLIFY = """
You are cleaning decompiler-generated C code.

Goal:
Make the code cleaner while preserving:
- exact behavior
- control flow structure
- loops, recursion, and conditionals
- function boundaries

Rules:
- Do NOT replace loops with constants
- Do NOT collapse recursion into precomputed values
- Do NOT remove branches unless they are clearly unreachable and unnecessary for valid C
- Do NOT change function behavior
- Do NOT invent helper functions
- Do NOT invent new variables unless required for valid C syntax
- Only simplify redundant temporaries, awkward syntax, and decompiler artifacts
- Preserve the overall program structure as much as possible
- Output ONLY valid C code
- No explanation
- No markdown fences

Code:
{code}
"""


PROMPT_RENAME = """
You are renaming variables in decompiler-generated C code.

Goal:
Improve readability without changing behavior.

Rules:
- Preserve exact behavior
- Rename only local variables and parameters whose meaning is very clear
- Do NOT rename function names
- Do NOT invent new variables
- Do NOT guess if uncertain
- Prefer no rename over a risky rename
- Return ONLY a JSON object mapping old names to new names
- If no safe renames exist, return {{}}

Code:
{code}
"""


PROMPT_COMMENT = """
Add concise comments to the following C code only when they clarify non-obvious logic.

Rules:
- Do NOT change the code
- Do NOT add excessive comments
- Do NOT comment obvious one-line statements
- Focus on loops, recursion, conditions, or tricky computations
- Output ONLY valid C code with comments inserted
- No explanation
- No markdown fences

Code:
{code}
"""


REFINE_TO_COMPILABLE = """
You are an expert C programmer cleaning decompiler-generated C-like code.

Your priorities, in order, are:
1. Produce compilable C code
2. Preserve the exact semantics and behavior
3. Preserve the original control flow and structure as much as possible
4. Improve readability only after the first three are satisfied

Rules:
- Do NOT change the program's behavior
- Do NOT replace loops, recursion, or conditionals with constant returns or simplified expressions unless the input already does that
- Do NOT invent helper functions
- Do NOT split or merge functions
- Do NOT introduce new variables unless required for valid C syntax
- Do NOT remove computations or control flow
- Keep function boundaries the same
- Keep the code as close as possible to the input structure while making it valid C
- Replace unknown decompiler-specific types with appropriate standard C types when reasonably clear
- Remove missing or unusable decompiler-specific includes if necessary for compilation
- Preserve function names unless changing them is necessary for valid standalone C
- Output ONLY valid C code
- No explanation
- No markdown fences

Code:
{code}
"""





