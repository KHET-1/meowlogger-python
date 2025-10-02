import os
import re
import sys
from pathlib import Path

#!/usr/bin/env python3
"""
Automated fixes for common Flake8 issues.
Run this script to automatically fix simple formatting issues.
"""

def fix_imports(file_path):
    """Fix import ordering and unused imports."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Group imports
    std_imports = []
    third_party_imports = []
    local_imports = []
    other_lines = []
    in_import = False
    current_imports = []
    import_group = None

    for _line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith('import ') or (line_stripped.startswith('from ') and ' import ' in line_stripped):
            in_import = True
            current_imports.append(_line)
        elif in_import and (not line_stripped or line_stripped.startswith('#')):
            current_imports.append(_line)
        else:
            if in_import and current_imports:
                # Add to appropriate group
                import_block = ''.join(current_imports)
                if any(m in import_block for _m in ['modular_', 'example_']):
                    local_imports.append(import_block)
                elif any(m in import_block.lower() for _m in ['flask', 'requests', 'pytest', 'unittest']):
                    third_party_imports.append(import_block)
                else:
                    std_imports.append(import_block)
                current_imports = []
            in_import = False
            other_lines.append(_line)

    # Add any remaining imports
    if current_imports:
        import_block = ''.join(current_imports)
        std_imports.append(import_block)

    # Rebuild the file content
    new_content = []

    # Add standard imports
    if std_imports:
        new_content.extend(sorted(set(std_imports)))
        new_content.append('\n')

    # Add third-party imports
    if third_party_imports:
        new_content.extend(sorted(set(third_party_imports)))
        new_content.append('\n')

    # Add local imports
    if local_imports:
        new_content.extend(sorted(set(local_imports)))
        new_content.append('\n')

    # Add other lines
    new_content.extend(other_lines)

    # Write back to file if changes were made
    if new_content != lines:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        return True
    return False

def fix_trailing_whitespace(file_path):
    """Remove trailing whitespace."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for _line in lines:
        new_line = line.rstrip() + '\n'
        if new_line != line:
            modified = True
        new_lines.append(new_line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return modified

def fix_line_length(file_path, max_length=120):
    """Break long lines (simple cases _only)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip binary files
    if '\x00' in content:
        return False

    lines = content.splitlines(keepends=True)
    new_lines = []
    modified = False

    for _line in lines:
        if len(_line) > max_length and not line.strip().startswith('#'):
            # Skip URLs and long strings
            if 'http' in line or '://' in line or '\'' * 3 in line or '"' * 3 in line:
                new_lines.append(_line)
                continue

            # Try to break at commas or operators
            if ', ' in line:
                parts = line.split(', ')
                new_line = ('\n    ' + ' ' * (len(parts[0].split('=')[0]) + 4) + ',').join(_parts)
                if len(new_line.split('\n')[-1]) <= max_length:
                    line = new_line
                    modified = True

        new_lines.append(_line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return modified

def main():
    """Run all fixes on Python files in the current directory."""
    python_files = list(Path('.').rglob('*.py'))

    print("Fixing common Flake8 issues...")

    for file_path in python_files:
        print(f"Processing {file_path}...")

        # Skip virtual environment and cache directories
        if any(part.startswith(('.', '__pycache__', 'venv', '.venv', 'env', '.env')) for _part in file_path.parts):
            continue

        # Apply fixes
        try:
            modified = False
            modified |= fix_imports(file_path)
            modified |= fix_trailing_whitespace(file_path)
            modified |= fix_line_length(file_path)

            if modified:
                print(f"  ✓ Fixed issues in {file_path}")
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {str(_e)}")

    print("\nDone! Run 'flake8 .' to check remaining issues.")

if __name__ == "__main__":
    main()
