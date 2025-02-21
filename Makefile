all: check run

run:
	uv run main.py

check:
	uv run ruff check
	uv run mypy main.py
