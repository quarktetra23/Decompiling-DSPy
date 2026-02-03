import os
from pathlib import Path
from dotenv import load_dotenv
import dspy

from decompile_dspy.pipeline import DecompileRefinePipeline

load_dotenv()

def main():
    # Configure DSPy LM.
    # import env variables from .env file

    lm = dspy.LM(model=os.getenv("DSPY_MODEL", "gpt-4o-mini"))  # example model name
    dspy.configure(lm=lm)

    sample_path = Path("data/sample_ghidra_output.c.txt")
    ghidra_code = sample_path.read_text(encoding="utf-8")

    pipe = DecompileRefinePipeline()
    out = pipe(ghidra_code=ghidra_code)

    print("====== FINAL C ======")
    print(out.final_c)
    print("\n====== DEBUG ======")
    print(out.debug)

if __name__ == "__main__":
    main()
