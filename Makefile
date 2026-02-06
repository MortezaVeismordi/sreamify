.PHONY: help dev-up dev-down build test migrate-all lint format clean

help:
	@echo "Available commands:"
	@echo "  make dev-up        - Start all services in development mode"
	@echo "  make dev-down      - Stop all services"
	@echo "  make build         - Build all Docker images"
	@echo "  make test          - Run all tests"
	@echo "  make migrate-all   - Run migrations for all services"
	@echo "  make lint          - Run linters on all services"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up temporary files"

dev-up:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml down

build:
	docker-compose -f docker/docker-compose.yml build

test:
	pytest tests/ --cov --cov-report=html

migrate-all:
	@echo "Running migrations for all services..."
	@bash scripts/migrate-all.sh

lint:
	flake8 services/ shared/
	black --check services/ shared/

format:
	black services/ shared/

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache .coverage htmlcov
