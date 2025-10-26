# Contributing to DocFitLabs for AI

Thank you for your interest in contributing to DocFitLabs for AI! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes**
5. **Test your changes**
6. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip

### Local Setup

```bash
# Clone your fork
git clone https://github.com/your-username/docfit4ai.git
cd docfit4ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_scoring_engine.py
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## 📝 Contribution Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions small and focused
- Use meaningful variable names

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add PII detection for credit cards
fix: resolve parsing error for PDF files
docs: update installation instructions
test: add unit tests for security analyzer
```

### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** with tests
3. **Update documentation** if needed
4. **Run tests** and ensure they pass
5. **Submit pull request** with clear description

### Pull Request Template

Use the provided template when creating pull requests:

- [ ] Description of changes
- [ ] Type of change (bug fix, feature, etc.)
- [ ] Testing performed
- [ ] Documentation updated
- [ ] Code follows style guidelines

## 🧪 Testing

### Writing Tests

- Write tests for new functionality
- Aim for high test coverage
- Test edge cases and error conditions
- Use descriptive test names

### Test Structure

```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_scoring_engine.py::test_calculate_score

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html
```

## 📚 Documentation

### Code Documentation

- Write docstrings for all public functions
- Include type hints
- Explain complex algorithms
- Provide usage examples

### User Documentation

- Update README.md for new features
- Add installation instructions
- Include usage examples
- Update API documentation

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description** of the bug
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment** (OS, Python version, etc.)
- **Screenshots** if applicable

## 💡 Feature Requests

When requesting features, please include:

- **Use case** and motivation
- **Detailed description**
- **Alternative solutions** considered
- **Additional context**

## 🏗️ Architecture

### Project Structure

```
docfit4ai/
├── src/
│   ├── docfit_core/          # Core functionality
│   ├── cli/                  # Command-line tools
│   └── ui/                   # Web interface
├── tests/                    # Test files
├── examples/                 # Example files
└── docs/                     # Documentation
```

### Core Components

- **Scoring Engine**: Main assessment logic
- **Parsers**: Document parsing functionality
- **CLI Tools**: Command-line interfaces
- **Web UI**: Streamlit interface

## 🔒 Security

### Security Considerations

- **No hardcoded secrets** in code
- **Validate all inputs** from users
- **Handle errors gracefully**
- **Follow security best practices**

### Reporting Security Issues

For security vulnerabilities, please email:
- **Email**: security@docfit.ai
- **Subject**: Security Vulnerability Report

## 📄 License

By contributing to DocFitLabs for AI, you agree that your contributions will be licensed under the MIT License.

## 🆘 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: team@docfit.ai for direct contact

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to DocFit for AI! 🚀
