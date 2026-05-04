import os
import sys
import dspy

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from decompile_dspy.pipeline import DecompileRefinePipeline

# -----------------------------
# CONFIG
# -----------------------------
POST_DIR = "post-pro"
REFINED_DIR = "refined"

# -----------------------------
# DSPy SETUP
# -----------------------------
def setup_dspy():
    lm = dspy.LM(
        model=os.getenv("DSPY_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    dspy.settings.configure(lm=lm)

# -----------------------------
# PROCESS SINGLE FILE
# -----------------------------
def process_file(idx):
    idx = int(idx)

    input_file = os.path.join(POST_DIR, f"test{idx}.c")
    output_file = os.path.join(REFINED_DIR, f"test{idx}.c")

    if not os.path.exists(input_file):
        print(f"[!] Missing file: {input_file}")
        return

    print(f"\n[+] Processing test{idx}")

    with open(input_file, "r") as f:
        code = f.read()

    print("\n--- INPUT CODE ---")
    print(code)

    # RUN DSPy PIPELINE
    pipe = DecompileRefinePipeline()
    result = pipe(angr_code=code)

    # IMPORTANT: extract final output
    refined = result.final_c

    os.makedirs(REFINED_DIR, exist_ok=True)

    with open(output_file, "w") as f:
        f.write(refined)

    print("\n--- REFINED CODE ---")
    print(refined)

    print(f"[✓] Saved → {output_file}")

# -----------------------------
# PROCESS ALL FILES
# -----------------------------
def process_all():
    if not os.path.exists(POST_DIR):
        print("[!] post-pro folder not found")
        return

    files = sorted([
        f for f in os.listdir(POST_DIR)
        if f.startswith("test") and f.endswith(".c")
    ])

    if not files:
        print("[!] No test files found in post-pro/")
        return

    for file in files:
        idx = file.replace("test", "").replace(".c", "")
        process_file(idx)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    setup_dspy()

    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        process_all()