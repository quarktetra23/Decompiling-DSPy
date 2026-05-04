import os
import sys
import subprocess

PRE_DIR = "pre-pro"
BIN_DIR = "data"
POST_DIR = "post-pro"
REFINED_DIR = "refined"


def get_test_files(test_id=None):
    if test_id is not None:
        name = f"test{test_id}.c"
        path = os.path.join(PRE_DIR, name)

        if not os.path.exists(path):
            print(f"[!] Missing test file: {path}")
            return []

        return [name]

    return sorted([
        f for f in os.listdir(PRE_DIR)
        if f.startswith("test") and f.endswith(".c")
    ])


def compile_all(test_id=None):
    os.makedirs(BIN_DIR, exist_ok=True)

    files = get_test_files(test_id)

    if not files:
        print("[!] No test files found in pre-pro/")
        return

    for file in files:
        src_path = os.path.join(PRE_DIR, file)
        binary_name = file.replace(".c", "")
        binary_path = os.path.join(BIN_DIR, binary_name)

        print(f"[+] Compiling {src_path} -> {binary_path}")

        cmd = [
            "gcc",
            "-O0",
            "-fno-stack-protector",
            src_path,
            "-o",
            binary_path,
        ]

        # Only add -no-pie on Linux.
        # macOS clang ignores it and gives warnings.
        if sys.platform.startswith("linux"):
            cmd.insert(3, "-no-pie")

        subprocess.run(cmd, check=True)


def run_angr_all(test_id=None):
    os.makedirs(POST_DIR, exist_ok=True)

    if test_id is not None:
        binaries = [f"test{test_id}"]
    else:
        binaries = sorted([
            f for f in os.listdir(BIN_DIR)
            if f.startswith("test") and not f.endswith(".c")
        ])

    if not binaries:
        print("[!] No binaries found in data/")
        return

    for binary in binaries:
        binary_path = os.path.join(BIN_DIR, binary)
        output_path = os.path.join(POST_DIR, f"{binary}.c")

        if not os.path.exists(binary_path):
            print(f"[!] Missing binary: {binary_path}")
            continue

        print(f"[+] Decompiling {binary_path} -> {output_path}")

        angr_script = f'''
import angr

binary_path = "{binary_path}"
output_path = "{output_path}"

proj = angr.Project(binary_path, auto_load_libs=False)
cfg = proj.analyses.CFGFast(normalize=True)

main_func = None

# macOS often stores main as _main.
for name in ["main", "_main"]:
    try:
        main_func = proj.kb.functions.function(name=name)
        if main_func is not None:
            break
    except Exception:
        pass

# fallback: search function names manually
if main_func is None:
    for func in proj.kb.functions.values():
        if func.name in ["main", "_main"]:
            main_func = func
            break

# final fallback: use entry function
if main_func is None:
    try:
        main_func = proj.kb.functions[proj.entry]
    except Exception:
        main_func = None

if main_func is None:
    code = "int main(void) {{ return 0; }}"
else:
    try:
        decompilation = proj.analyses.Decompiler(main_func, cfg=cfg)
        if decompilation.codegen is None:
            code = "int main(void) {{ return 0; }}"
        else:
            code = decompilation.codegen.text
    except Exception as e:
        code = "int main(void) {{ return 0; }}"

with open(output_path, "w") as f:
    f.write(code)
'''

        subprocess.run(
            [sys.executable, "-c", angr_script],
            check=True
        )


def run_dspy(test_id=None):
    cmd = [sys.executable, "scripts/run_refine.py"]

    if test_id is not None:
        cmd.append(str(test_id))

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    test_id = None

    if len(sys.argv) > 1:
        test_id = sys.argv[1]

    print("\n=== STEP 1: COMPILING C TEST CASES ===")
    compile_all(test_id)

    print("\n=== STEP 2: GENERATING ANGR OUTPUTS ===")
    run_angr_all(test_id)

    print("\n=== STEP 3: RUNNING DSPY REFINEMENT ===")
    run_dspy(test_id)

    print("\nupdated")