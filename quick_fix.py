#!/usr/bin/env python3
"""Quick fix for remaining syntax issues."""

import re


def fix_file(filename):
    """Fix syntax issues in a single file."""
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix malformed __init__ docstrings
    content = re.sub(
        r"(\s+)def __init__\([^)]*\):\s*\n(\s+)\"\"\"__init__ function\.\s*\n\s*\n\s*Args:\s*\n\s*TODO: Add arguments\s*\n\s*\"\"\"",
        r'\1def __init__(self):\n\2"""Initialize instance."""\n\2pass',
        content,
        flags=re.MULTILINE,
    )

    # Fix malformed process docstrings
    content = re.sub(
        r"(\s+)def process\([^)]*\):\s*\n(\s+)\"\"\"process function\.\s*\n\s*\n\s*Args:\s*\n\s*TODO: Add arguments\s*\n\s*\"\"\"",
        r'\1def process(self, entry):\n\2"""Process log entry."""\n\2pass',
        content,
        flags=re.MULTILINE,
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {filename}")


# Fix all Python files
import glob

for file in glob.glob("*.py"):
    if file not in ["fix_docstrings.py", "quick_fix.py"]:
        try:
            fix_file(file)
        except Exception as e:
            print(f"Error fixing {file}: {e}")
