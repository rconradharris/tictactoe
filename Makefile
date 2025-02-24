all: play

play:
	uv run main.py play

debug:
	uv run main.py debug

test:
	uv run main.py test

check:
	uv run ruff check
	uv run mypy .
