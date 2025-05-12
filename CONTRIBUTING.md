# Contributing to Brain Mapping EEG Classification System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/your-username/brain-mapping-eeg.git
cd brain-mapping-eeg
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting
- Add type hints where appropriate
- Write descriptive commit messages

## Testing

Run tests before submitting:
```bash
pytest tests/ -v
```

## Pull Request Process

1. Update documentation for significant changes
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Questions?

Open an issue or contact the maintainers.
