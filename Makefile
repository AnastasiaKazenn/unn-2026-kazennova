.PHONY: test format lint typecheck check build

test:
	uv run python -m unittest discover -s tests -v

format:
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run mypy bot/ main.py

check: lint typecheck test

build:
	docker build -t echo-bot .