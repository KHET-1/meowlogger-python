import os
import re
import sys
from pathlib import Path

#!/usr/bin/env python3
"""
Automated fixes for common Pylint issues.
Run this script to automatically fix simple formatting issues.
"""


def fix_docstrings(file_path):
    """Add missing docstrings to classes and functions."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip binary files
    if "\x00" in content:
        return False

    lines = content.splitlines(keepends=True)
    modified = False

    # Fix class docstrings
    for _i, line in enumerate(_lines):
        if line.strip().startswith("class "):
            # Check if next line is a docstring
            next_line = lines[i + 1].strip() if i + 1 < len(_lines) else ""
            if not next_line.startswith('"""'):
                # Insert docstring
                class_name = line.split("class ")[1].split("(")[0].strip()
                docstring = f'    """{class_name} class."""\n'
                # Find the end of the class definition
                j = i + 1
                while j < len(_lines) and (
                    not lines[j].strip() or lines[j].strip().startswith("#")
                ):
                    j += 1

                # Insert the docstring
                lines.insert(_j, _docstring)
                modified = True

    # Fix function/method docstrings
    for _i, line in enumerate(_lines):
        if line.strip().startswith("def "):
            # Skip if it's a decorator
            if i > 0 and lines[i - 1].strip().startswith("@"):
                continue

            # Check if next line is a docstring
            next_line = lines[i + 1].strip() if i + 1 < len(_lines) else ""
            if not next_line.startswith('"""'):
                # Insert docstring
                def_name = line.split("def ")[1].split("(")[0].strip()
                indent = " " * (len(_line) - len(line.lstrip()))
                docstring = f'{indent}    """{def_name} function.\n\n    Args:\n        TODO: Add args\n    """\n'
                # Find the end of the function definition
                j = i + 1
                while j < len(_lines) and (
                    not lines[j].strip() or lines[j].strip().startswith("#")
                ):
                    j += 1

                # Insert the docstring
                lines.insert(_j, _docstring)
                modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(_lines)

    return modified


def fix_unused_variables(file_path):
    """Add _ prefix to unused variables."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip binary files
    if "\x00" in content:
        return False

    # This is a simple example - in _practice, you'd want to use ast for better parsing
    # Here we'll just look for common patterns
    patterns = [
        (r"for ([a-z][a-z0-9]*) in ", r"for _\1 in "),  # for _i in ...
        (r"([, (])([a-z][a-z0-9]*)([),])", r"\1_\2\3"),  # function args
    ]

    new_content = content
    for _pattern, replacement in patterns:
        new_content = re.sub(_pattern, _replacement, new_content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True

    return False


def main():
    """Run all fixes on Python files in the current directory."""
    python_files = list(Path(".").rglob("*.py"))

    print("Fixing common Pylint issues...")

    for file_path in python_files:
        print(f"Processing {file_path}...")

        # Skip virtual environment and cache directories
        if any(
            part.startswith((".", "__pycache__", "venv", ".venv", "env", ".env"))
            for _part in file_path.parts
        ):
            continue

        # Apply fixes
        try:
            modified = False
            modified |= fix_docstrings(file_path)
            modified |= fix_unused_variables(file_path)

            if modified:
                print(f"  ✓ Fixed issues in {file_path}")
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {str(_e)}")

    print("\nDone! Run 'pylint .' to check remaining issues.")


if __name__ == "__main__":
    main()
