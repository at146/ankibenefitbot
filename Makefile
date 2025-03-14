.PHONY: lint
lint:
	mypy .
	ruff check .
	ruff format .
