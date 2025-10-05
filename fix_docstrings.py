#!/usr/bin/env python3
"""Quick script to fix malformed docstrings."""

import glob
import re


def fix_docstrings():
    """Fix malformed docstrings in Python files."""
    files = glob.glob("*.py")

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Fix malformed __init__ docstrings
            content = re.sub(
                r"(\s+)def __init__\([^)]*\):\s*\n(\s+)\"\"\"__init__ function\.\s*\n\s*\n\s*Args:\s*\n\s*TODO: Add arguments\s*\n\s*\"\"\"",
                r'\1def __init__(self, *args, **kwargs):\n\2"""Initialize instance."""\n\2pass',
                content,
                flags=re.MULTILINE,
            )

            # Fix malformed process function docstrings
            content = re.sub(
                r"(\s+)def process\([^)]*\):\s*\n(\s+)\"\"\"process function\.\s*\n\s*\n\s*Args:\s*\n\s*TODO: Add arguments\s*\n\s*\"\"\"",
                r'\1def process(self, entry):\n\2"""Process log entry."""\n\2pass',
                content,
                flags=re.MULTILINE,
            )

            if content != original_content:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed docstrings in {file}")
            else:
                print(f"No fixes needed in {file}")

        except Exception as e:
            print(f"Error fixing {file}: {e}")


if __name__ == "__main__":
    fix_docstrings()
