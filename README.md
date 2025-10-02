# MeowLogger 🐱

A modular, high-quality logging system with comprehensive quality gates and automated testing.

## Features

- **Modular Architecture**: Clean separation of concerns with pluggable components
- **Quality Gates**: Automated code quality, security, and testing checks
- **Comprehensive Testing**: Full test coverage with multiple testing strategies
- **Type Safety**: Full type annotations with mypy checking
- **Security**: Automated security scanning with bandit and safety
- **Code Quality**: Automated formatting, linting, and complexity analysis

## Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd meowlogger

# Install development dependencies
make install-dev

# Run quality gates
make quality-gate

# Run tests
make test
```

## Project Structure

```
meowlogger/
├── modular_core.py              # Core logging system
├── modular_web_interface.py     # Web interface components
├── example-app-launcher.py      # Example usage
├── quality-tests-complete.py    # Comprehensive test suite
├── .github/workflows/           # GitHub Actions CI/CD
├── pyproject.toml              # Project configuration
└── requirements-dev.txt         # Development dependencies
```

## Quality Gates

This project enforces strict quality standards through automated checks:

### Code Formatting
- **Black**: Consistent code formatting
- **isort**: Import sorting and organization

### Linting & Type Checking
- **flake8**: Style guide enforcement
- **pylint**: Advanced code analysis
- **mypy**: Static type checking

### Security
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability checking

### Code Quality
- **radon**: Cyclomatic complexity analysis
- **xenon**: Maintainability index monitoring

### Testing
- **pytest**: Comprehensive test suite
- **pytest-cov**: Coverage reporting
- **Multiple test strategies**: Unit, integration, and quality tests

## Available Commands

```bash
make help              # Show all available commands
make install           # Install production dependencies
make install-dev       # Install development dependencies
make test              # Run tests with coverage
make lint              # Run all linters
make format            # Format code
make check-quality     # Run quality checks
make security          # Run security checks
make quality-gate      # Run complete quality gate
make clean             # Clean build artifacts
make ci                # Run CI pipeline locally
```

## CI/CD Pipeline

The GitHub Actions workflow automatically runs on:
- Push to main/develop branches
- Pull requests

Quality checks include:
1. **Multi-Python Testing**: Python 3.8, 3.9, 3.10, 3.11
2. **Code Formatting**: Black and isort validation
3. **Linting**: flake8, pylint, mypy
4. **Security**: bandit and safety scanning
5. **Testing**: pytest with coverage reporting
6. **Quality**: Complexity and maintainability analysis

## Development Setup

1. **Pre-commit Hooks**: Automatically run quality checks before commits
2. **Local Testing**: Run `make ci` to test the full pipeline locally
3. **IDE Integration**: Configure your IDE to use the project's formatting and linting settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make quality-gate` to ensure all checks pass
5. Submit a pull request

All contributions must pass the complete quality gate before being merged.

## License

MIT License - see LICENSE file for details.