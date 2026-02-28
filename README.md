# State Machine Framework

Small example project implementing **simple state machine framework** in
**Python**.

This framework includes/supports:

- **Abstract base class** for state machines,
- **Defining states and trigger events**,
- **Defining transitions** between states with associated events and callbacks,
- **Handling events** to trigger state transitions.

Check out the code in [src/state_machine/](src/state_machine) for details.

## Quick start

1. Ensure you have Python 3.12+ installed (matching `pyproject.toml`).

2. Install [`uv`](https://docs.astral.sh/uv/) (once, globally):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3. From the project root, create the virtual environment and install dependencies:
    ```bash
    uv sync
    ```

4. Run the demo script inside the `uv` environment:
    ```bash
    uv run python src/main.py
    ```

## Developer setup

### Pre-commit hooks

This project uses [`pre-commit`](https://pre-commit.com) (installed via the `dev` dependency group in `pyproject.toml`)
to run tools like `ruff` and `ty` before each commit.

1. Install dev dependencies (if you haven’t already):
    ```bash
    uv sync --group dev
    ```

2. Install the Git hooks:
    ```bash
    uv run pre-commit install
    ```

3. (Optional) Run all hooks on the codebase:
    ```bash
    uv run pre-commit run --all-files
    ```
