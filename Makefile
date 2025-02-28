all: check tests

fmt:
	uv run black .

check:
	uv run ruff check
	uv run mypy .

.PHONY: tests
tests:
	uv run main.py tests
