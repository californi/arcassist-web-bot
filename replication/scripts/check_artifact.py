"""Lightweight release-hygiene check for the camera-ready artifact."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SECRET_PATTERNS = [
    re.compile(r"gsk_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}"),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
]
GENERATED_FILES = {
    Path("rag/index.faiss"),
    Path("rag/docs.npy"),
}
FORBIDDEN_METADATA = {".DS_Store"}
TEXT_SUFFIXES = {
    ".py", ".txt", ".md", ".html", ".css", ".yml", ".yaml", ".example", ".cff"
}


def main() -> int:
    issues: list[str] = []

    for generated in GENERATED_FILES:
        if (ROOT / generated).exists():
            issues.append(f"Remove generated file before release: {generated}")

    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue

        relative = path.relative_to(ROOT)

        if path.name == ".env":
            issues.append(f"Do not publish {relative}")
            continue

        if path.name in FORBIDDEN_METADATA:
            issues.append(f"Remove OS/editor metadata: {relative}")

        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README.md", ".gitignore", ".gitattributes"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    issues.append(f"Potential secret-like token in {relative}")
            # Skip local-path pattern matching against this checker itself because
            # the regex definitions intentionally contain those path fragments.
            if relative.as_posix() != "replication/scripts/check_artifact.py":
                for pattern in LOCAL_PATH_PATTERNS:
                    if pattern.search(text):
                        issues.append(f"Potential local path leakage in {relative}")

    if issues:
        print("\n".join(issues))
        return 1

    print("Camera-ready artifact check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
