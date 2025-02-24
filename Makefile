all: play

play:
	uv run main.py play

debug:
	uv run main.py debug

test:
	uv run main.py test ${TEST}

.PHONY: tests
tests:
	uv run main.py tests

check:
	uv run ruff check
	uv run mypy .
