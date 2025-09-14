.PHONY: uv-sync lint fmt test

uv-sync:
	uv pip install -e .
	uv pip install -e ".[dev]"

lint:
	uvx ruff check .

fmt:
	uvx ruff format .

test:
	pytest -q
