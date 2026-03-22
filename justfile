[private]
default:
   @just --list

# Run taplo, ruff, basedpyright, and mdformat in check mode
check:
    uv run taplo fmt --check pyproject.toml
    uv run ruff format --check --preview
    uv run ruff check
    uv run basedpyright src scripts
    uv run mdformat --number --wrap 80 --check README.md

# Run taplo, ruff's formatter, and mdformat
format:
    uv run taplo fmt pyproject.toml
    uv run ruff format --preview
    uv run mdformat --number --wrap 80 README.md

# Format + run ruff in fix mode
fix: format
    uv run ruff check --fix

# Regenerate imports, model, and endpoint definitions
codegen:
    uv run scripts/codegen.py
    uv run ruff format
