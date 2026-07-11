from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SECRET_PATTERNS = [
    re.compile("gsk_[A-Za-z0-9_\\-]{12,}"),
    re.compile("sk-[A-Za-z0-9_\\-]{12,}"),
]
LOCAL_PATH_TOKEN = "/" + "Users/"


def main() -> int:
    issues = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.name == ".env":
            issues.append(f"Do not publish {path.relative_to(ROOT)}")
            continue
        if path.suffix.lower() in {".py", ".txt", ".md", ".html", ".css", ".yml", ".yaml", ".example"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    issues.append(f"Potential secret-like token in {path.relative_to(ROOT)}")
            if LOCAL_PATH_TOKEN in text:
                issues.append(f"Potential local path leakage in {path.relative_to(ROOT)}")
    if issues:
        print("\n".join(issues))
        return 1
    print("Artifact check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
