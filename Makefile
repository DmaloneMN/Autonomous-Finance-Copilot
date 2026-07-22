.PHONY: install dev lint test build run clean

install:
	pip install -e .[dev]

pre-commit:
	pre-commit install

lint:
	ruff check src tests
	mypy src

format:
	ruff format src tests

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

build:
	docker build -t autonomous-finance-copilot:latest .

run:
	docker-compose up --build

run-dev:
	uvicorn src.main:app --reload --port 8000

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name '*.pyc' -delete
	rm -rf dist/ build/ .coverage coverage.xml htmlcov/
