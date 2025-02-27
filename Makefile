all: check tests

check:
	uv run ruff check
	uv run mypy .

.PHONY: tests
tests:
	uv run main.py tests
