#!/bin/bash

# Exit on error
set -e

echo "=== Installing dependencies ==="
pip install -r requirements-dev.txt

echo -e "\n=== Running Black formatter ==="
python -m black .

echo -e "\n=== Running Flake8 ==="
python -m flake8 .

echo -e "\n=== Running Pylint ==="
python -m pylint --rcfile=.pylintrc modular_*.py

echo -e "\n=== Running MyPy ==="
python -m mypy .

echo -e "\n=== Running Bandit ==="
python -m bandit -r .

echo -e "\n=== All checks passed! ==="
