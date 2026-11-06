.PHONY: lint format-check test check

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

test:
	uv run pytest

check: lint format-check test