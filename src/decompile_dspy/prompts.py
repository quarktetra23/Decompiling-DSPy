R_REF_PROMPT = """Do you think the following C code needs structure simplification, comment appending, and variable renaming?
Answer three yes or no in order. No explanation.

C CODE:
{code}
"""

PROMPT_SIMPLIFY = """Simplify the following C function by removing redundant variables and unnecessary code. No explanation.

C CODE:
{code}
"""

PROMPT_RENAME = """Help me rename the variables for the code snippet in the following C code.
Output the old and new names in JSON format like {{'old name': 'new name'}}. No explanation.

C CODE:
{code}
"""

PROMPT_COMMENT = """Help me add code comments for the code snippet in the following C code.
No explanation.

C CODE:
{code}
"""

REFINE_TO_COMPILABLE = """Convert the following decompiler pseudo-C into clean, Linux-compilable C.
Constraints:
- Do NOT use goto.
- Add missing #include headers if needed.
- Keep behavior identical to the pseudo-code.
- Prefer for/while loops over deeply nested do/while when reasonable.
- Output ONLY the final C code, no explanation.

PSEUDO-C:
{code}
"""
