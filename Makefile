.PHONY: lint format format-check fix test check

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

test:
	uv run pytest

check: lint format-check test

format:
	uv run ruff format .

fix:
	uv run ruff check --fix .
	uv run ruff format .
