PYTHON ?= python3

.PHONY: install lint test security train evaluate serve pipeline docker-up docker-down clean

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check src tests
	mypy src

test:
	pytest

security:
	bandit -q -r src
	pip-audit

train:
	$(PYTHON) -m mlops_pipeline.training.train --config configs/training.yaml

evaluate:
	$(PYTHON) -m mlops_pipeline.training.evaluate --config configs/training.yaml

serve:
	uvicorn mlops_pipeline.serving.app:app --host 0.0.0.0 --port 8000

pipeline:
	$(PYTHON) -m mlops_pipeline.pipeline

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov dist build
