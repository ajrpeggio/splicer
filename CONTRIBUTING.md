
# Contributing to Splicer

Thank you for considering contributing to **Splicer**! We welcome contributions to improve the project, whether it's fixing bugs, adding features, or improving documentation.

## Getting Started

To start contributing, please follow these steps:

1. Fork the repository to your GitHub account.
2. Clone your forked repository:
   ```bash
   git clone https://github.com/<your-username>/splicer.git
   cd splicer
   ```
3. Create a new branch for your changes:
   ```bash
   git checkout -b feature/my-new-feature
   ```

## Setting Up the Development Environment

1. Ensure you have Python 3.7 or later installed.
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Before submitting a pull request, ensure all tests pass:

1. Install test dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Run the tests:
   ```bash
   pytest
   ```

## Code Style

We follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style. Please run `flake8` or `black` to ensure your code adheres to the style guide:

- Install style dependencies:
  ```bash
  pip install flake8 black
  ```
- Run code style checks:
  ```bash
  flake8
  black --check .
  ```

## Submitting a Pull Request

1. Push your branch to your forked repository:
   ```bash
   git push origin feature/my-new-feature
   ```
2. Open a pull request on the main repository.
3. In your pull request, include a clear and concise description of your changes.
4. Ensure the CI checks pass.

## Publishing to Test PyPI

For testing purposes, you can publish the package to Test PyPI:

1. Build the distribution:
   ```bash
   python -m build
   ```
2. Upload the distribution to Test PyPI:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
3. Use the `--repository-url` flag if you encounter issues.

Thank you for contributing! 🎉