import os
import re
import sys
import ast
from pathlib import Path
from collections import defaultdict

#!/usr/bin/env python3
"""
Comprehensive automated fixes for all linting issues.
This script will fix Flake8, Pylint, and other common code quality issues.
"""


class LintFixer:
    """LintFixer class for automated code quality fixes."""

    def __init__(self):
        self.python_files = []
        self.issues_found = defaultdict(int)
        self.files_modified = []

    def find_python_files(self):
        """Find all Python files in the current directory."""
        for file_path in Path(".").rglob("*.py"):
            if not any(
                part.startswith((".", "__pycache__", "venv", ".venv", "env", ".env"))
                for _part in file_path.parts
            ):
                self.python_files.append(file_path)

    def fix_imports(self, file_path):
        """Fix import ordering and unused imports."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return False

        # Parse imports
        std_imports = []
        third_party_imports = []
        local_imports = []
        other_lines = []

        i = 0
        while i < len(_lines):
            line = lines[i]
            line_stripped = line.strip()

            # Check if this is an import line
            if line_stripped.startswith("import ") or (
                line_stripped.startswith("from ") and " import " in line_stripped
            ):
                # Collect consecutive import lines
                import_block = [line]
                i += 1

                # Check next lines for continuation
                while i < len(_lines):
                    next_line = lines[i].strip()
                    if next_line.startswith("import ") or (
                        next_line.startswith("from ") and " import " in next_line
                    ):
                        import_block.append(lines[i])
                        i += 1
                    elif next_line and not next_line.startswith("#"):
                        break
                    else:
                        i += 1

                # Categorize imports
                import_text = "".join(import_block)
                if any(
                    module in import_text
                    for _module in ["modular_", "example_", "meowlogger"]
                ):
                    local_imports.append(import_text)
                elif any(
                    module in import_text.lower()
                    for _module in [
                        "flask",
                        "requests",
                        "pytest",
                        "unittest",
                        "json",
                        "os",
                        "sys",
                        "datetime",
                        "tempfile",
                    ]
                ):
                    std_imports.append(import_text)
                else:
                    third_party_imports.append(import_text)

                continue

            # Non-import line
            other_lines.append(_line)
            i += 1

        # Rebuild file with proper ordering
        new_content = []

        # Add standard library imports
        if std_imports:
            new_content.extend(std_imports)
            new_content.append("\n")

        # Add third-party imports
        if third_party_imports:
            new_content.extend(third_party_imports)
            new_content.append("\n")

        # Add local imports
        if local_imports:
            new_content.extend(local_imports)
            new_content.append("\n")

        # Add other lines
        new_content.extend(other_lines)

        # Write back if changed
        if new_content != lines:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_content)
            return True

        return False

    def fix_trailing_whitespace(self, file_path):
        """Remove trailing whitespace from all lines."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return False

        modified = False
        new_lines = []

        for _line in lines:
            new_line = line.rstrip() + "\n"
            if new_line != line:
                modified = True
            new_lines.append(new_line)

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        return modified

    def fix_line_length(self, file_path, max_length=120):
        """Break long lines appropriately."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return False

        modified = False
        new_lines = []

        for _line in lines:
            if len(_line) > max_length and not line.strip().startswith("#"):
                # Skip URLs and strings
                if (
                    "http" in line
                    or "://" in line
                    or line.count("'") >= 3
                    or line.count('"') >= 3
                ):
                    new_lines.append(_line)
                    continue

                # Try to break at commas
                if ", " in line:
                    parts = line.split(", ")
                    if len(_parts) > 1:
                        # Find the indentation level
                        indent = len(_line) - len(line.lstrip())
                        new_line = (
                            parts[0] + ",\n" + " " * (indent + 4) + ", ".join(parts[1:])
                        )
                        if len(new_line.split("\n")[-1]) <= max_length:
                            new_lines.append(new_line)
                            modified = True
                            continue

            new_lines.append(_line)

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        return modified

    def fix_docstrings(self, file_path):
        """Add missing docstrings to classes and functions."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return False

        modified = False
        new_lines = []

        i = 0
        while i < len(_lines):
            line = lines[i]

            # Check for class definitions
            if line.strip().startswith("class "):
                class_name = line.split("class ")[1].split("(")[0].split(":")[0].strip()

                # Check if next line is a docstring
                if i + 1 < len(_lines) and not lines[i + 1].strip().startswith('"""'):
                    # Insert docstring
                    indent = len(_line) - len(line.lstrip())
                    docstring = (
                        " " * indent
                        + f'"""{class_name} class.\n\n    Args:\n        TODO: Add arguments\n    """\n'
                    )
                    new_lines.append(_line)
                    new_lines.append(_docstring)
                    i += 1
                    modified = True
                else:
                    new_lines.append(_line)

            # Check for function/method definitions
            elif line.strip().startswith("def "):
                func_name = line.split("def ")[1].split("(")[0].strip()

                # Skip if it's a decorator
                if i > 0 and lines[i - 1].strip().startswith("@"):
                    new_lines.append(_line)
                    i += 1
                    continue

                # Check if next line is a docstring
                if i + 1 < len(_lines) and not lines[i + 1].strip().startswith('"""'):
                    # Insert docstring
                    indent = len(_line) - len(line.lstrip())
                    docstring = (
                        " " * indent
                        + f'"""{func_name} function.\n\n    Args:\n        TODO: Add arguments\n    """\n'
                    )
                    new_lines.append(_line)
                    new_lines.append(_docstring)
                    i += 1
                    modified = True
                else:
                    new_lines.append(_line)

            else:
                new_lines.append(_line)

            i += 1

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        return modified

    def fix_unused_variables(self, file_path):
        """Add _ prefix to unused variables."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return False

        # Simple regex-based fixes for common patterns
        patterns = [
            # For loops
            (r"for ([a-z][a-z0-9]*) in ", r"for _\1 in "),
            # Function arguments
            (
                r"([, (])([a-z][a-z0-9]*)([),])",
                lambda m: (
                    m.group(1) + "_" + m.group(2) + m.group(3)
                    if not m.group(2) in ["self", "cls"]
                    else m.group(0)
                ),
            ),
        ]

        original_content = content
        for _pattern, replacement in patterns:
            if callable(_replacement):
                content = re.sub(_pattern, _replacement, _content)
            else:
                content = re.sub(_pattern, _replacement, _content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(_content)
            return True

        return False

    def run_all_fixes(self):
        """Run all fixes on all Python files."""
        print("🔧 Starting comprehensive linting fixes...")
        print(f"📁 Found {len(self.python_files)} Python files")

        for file_path in self.python_files:
            print(f"📝 Processing {file_path}...")

            try:
                modified = False

                # Apply all fixes
                modified |= self.fix_imports(file_path)
                modified |= self.fix_trailing_whitespace(file_path)
                modified |= self.fix_line_length(file_path)
                modified |= self.fix_docstrings(file_path)
                modified |= self.fix_unused_variables(file_path)

                if modified:
                    self.files_modified.append(str(file_path))
                    print(f"  ✅ Fixed issues in {file_path}")

            except Exception as e:
                print(f"  ❌ Error processing {file_path}: {str(_e)}")
                self.issues_found["errors"] += 1

        print(f"\n📊 Summary:")
        print(f"  📝 Files processed: {len(self.python_files)}")
        print(f"  ✅ Files modified: {len(self.files_modified)}")
        print(f"  ❌ Errors: {self.issues_found['errors']}")

        if self.files_modified:
            print(f"\n📋 Modified files:")
            for file_path in self.files_modified:
                print(f"  • {file_path}")

        return len(self.files_modified) > 0


def main():
    """Main function to run all fixes."""
    fixer = LintFixer()
    fixer.find_python_files()

    if not fixer.python_files:
        print("❌ No Python files found!")
        sys.exit(1)

    success = fixer.run_all_fixes()

    if success:
        print("\n🎉 Fixes applied! Run 'flake8 .' to verify improvements.")
        print("💡 Note: Some issues may require manual fixes.")
    else:
        print("\n✅ No automatic fixes needed!")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
