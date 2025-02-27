all: play

play:
	uv run main.py play

debug:
	uv run main.py debug

.PHONY: battle
battle:
	uv run main.py battle ${n}

file_test:
	uv run main.py file_test ${test}

.PHONY: tests
tests:
	uv run main.py tests

check:
	uv run ruff check
	uv run mypy .
