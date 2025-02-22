all: play

play:
	uv run main.py play

test:
	uv run main.py test

check:
	uv run ruff check
	uv run mypy .
