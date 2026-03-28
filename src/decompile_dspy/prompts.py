R_REF_PROMPT = """Do you think the following C code needs structure simplification, comment appending, and variable renaming?
Answer three yes or no in order. No explanation.

C CODE:
{code}
"""

PROMPT_SIMPLIFY = """
Clean and simplify the following C code while preserving:
- exact behavior
- control flow structure
- loops, recursion, and conditionals

Rules:
- Do NOT replace loops with constants
- Do NOT collapse recursion into precomputed values
- Do NOT remove branches unless they are clearly dead and unnecessary for compilation
- Do NOT change function behavior
- Only simplify redundant variable usage, awkward syntax, and Ghidra artifacts
- Output ONLY valid C code, with no explanation and no markdown fences

Code:
{code}
"""

PROMPT_RENAME = """
Rename variables in the following C code conservatively.

Rules:
- Preserve exact behavior
- Only rename variables if the meaning is very clear
- Do NOT invent new variables
- Do NOT rename function names
- Do NOT rename anything if uncertain
- Return ONLY a JSON object mapping old variable names to new variable names
- If no safe renames exist, return {}

Code:
{code}
"""

PROMPT_COMMENT = """Help me add code comments for the code snippet in the following C code.
No explanation.

C CODE:
{code}
"""

REFINE_TO_COMPILABLE = """
You are an expert C programmer helping clean up Ghidra decompiled C code.

Your priorities, in order, are:
1. Produce compilable C code
2. Preserve the exact semantics and behavior
3. Preserve the original control flow and structure as much as possible
4. Improve readability only after the first three are satisfied

Rules:
- Do NOT change the program's behavior
- Do NOT replace loops, recursion, or conditionals with constant returns or simplified expressions unless the input already does that
- Do NOT invent new helper functions
- Do NOT introduce new variables unless required for valid C syntax
- Do NOT remove computations or control flow
- Keep function boundaries the same
- Keep the code as close as possible to the input structure while making it valid C
- Remove or replace unknown Ghidra-specific types like undefined4 with appropriate C types
- If an include like out.h is missing, rewrite the code so it compiles without that header
- Output ONLY valid C code, with no explanation and no markdown fences

Code:
{code}
"""







