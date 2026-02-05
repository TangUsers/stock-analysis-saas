# Contributing to Stock Analysis SaaS

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🏗️ Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. **Fork** the repo and create your branch from `main`
2. **Clone** your fork locally
3. **Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **Make your changes** and ensure tests pass
5. **Commit** your changes with a clear message
6. **Push** to your fork
7. **Open a Pull Request** against the `main` branch

## 📋 Code Style

### Python

We follow PEP 8 guidelines with some modifications:

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints for all function signatures
- Write docstrings for all public modules, functions, classes, and methods

```python
def example_function(param: str, param2: int) -> bool:
    """Short description of the function.

    Args:
        param: Description of param
        param2: Description of param2

    Returns:
        Description of return value
    """
    # Your code here
    return True
```

### Testing

- All new features should include appropriate tests
- Run tests before submitting: `pytest tests/`
- Maintain or increase code coverage

```python
def test_example():
    """Test example function."""
    assert example_function("test", 1) == True
```

## 🔧 Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stock-analysis-saas.git
cd stock-analysis-saas

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy

# Install pre-commit hooks (optional)
pre-commit install
```

## 📝 Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(analysis): add new moving average calculation

- Added exponential moving average (EMA)
- Improved calculation performance by 40%
- Added unit tests for EMA

Closes #123
```

## 🐛 Reporting Bugs

We use GitHub issues for bug reports. To report a bug:

1. **Search** existing issues to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include**:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected behavior vs actual behavior
   - Python version and operating system
   - Any relevant error messages or screenshots

## 💡 Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Search** existing feature requests
2. **Use the feature request template**
3. **Explain** why this feature would be useful
4. **Provide** use cases or examples
5. **Consider** implementation complexity

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- Our README.md contributors section
- Release notes
- GitHub's contributor graph

Thank you for contributing to Stock Analysis SaaS! 🎉
