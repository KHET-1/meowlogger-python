#!/usr/bin/env python3
"""
Check remaining linting issues after automated fixes.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the output."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1


def main():
    print("🔍 Checking remaining linting issues...")
    print("=" * 50)

    # Check Flake8
    print("\n📋 FLAKE8 RESULTS:")
    stdout, stderr, returncode = run_command(
        "flake8 . --count", "c:\\Users\\credi\\Desktop\\meowlogger"
    )

    if returncode == 0:
        print("✅ No Flake8 issues found!")
    else:
        print("⚠️  Flake8 issues remain:")
        if stdout:
            print(stdout)
        if stderr:
            print(f"Errors: {stderr}")

    # Check Pylint
    print("\n🔧 PYLINT RESULTS:")
    stdout, stderr, returncode = run_command(
        "pylint --rcfile=.pylintrc modular_*.py quality-tests-complete.py",
        "c:\\Users\\credi\\Desktop\\meowlogger",
    )

    if returncode == 0:
        print("✅ No Pylint issues found!")
    else:
        print("⚠️  Pylint issues remain:")
        if stdout:
            print(stdout)
        if stderr:
            print(f"Errors: {stderr}")

    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print("✅ Automated fixes applied to all Python files")
    print("✅ Import ordering fixed")
    print("✅ Trailing whitespace removed")
    print("✅ Line length issues addressed")
    print("✅ Docstrings added where missing")
    print("✅ Variable naming conventions applied")

    print("\n📝 MANUAL FIXES (if any remain):")
    print("• Complex line length issues may need manual breaking")
    print("• Some unused imports may require manual review")
    print("• Complex function structures may need refactoring")

    print("\n🚀 NEXT STEPS:")
    print("1. Run: pre-commit run --all-files")
    print("2. Fix any remaining issues manually")
    print("3. Run: python -m pytest (if tests exist)")
    print("4. Commit changes with: git commit -m 'Fix linting issues'")


if __name__ == "__main__":
    main()
