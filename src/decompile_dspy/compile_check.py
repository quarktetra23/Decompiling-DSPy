import subprocess
import tempfile
from pathlib import Path

def gcc_syntax_check(c_code: str) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        c_path = td / "out.c"
        c_path.write_text(c_code, encoding="utf-8")

        cmd = ["gcc", "-std=c11", "-Wall", "-Wextra", "-fsyntax-only", str(c_path)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        ok = (p.returncode == 0)
        msg = (p.stdout or "") + (p.stderr or "")
        return ok, msg.strip()
