# Makefile API Cost Map
DOCKER_IMAGE_NAME = api-cost-map-web
DOCKER_CONTAINER_NAME = api-cost-map
PORT = 8000
DOCKER_TAG=1.0.0
IMAGE_API = $(DOCKER_IMAGE_NAME)-api:$(DOCKER_TAG)
DEV_COMPOSE = docker-compose.dev.yaml
PROD_COMPOSE = docker-compose.prod.yaml
DB_CONTAINER_NAME = mysql-server
DB_PORT = 3306
DB_NAME = costdb
DB_USER = admin
DB_PASS = pass


build-dev:
	chmod +x entrypoint.sh
	IMAGE_API=$(IMAGE_API) docker compose -f $(DEV_COMPOSE) build

up-dev:
	IMAGE_API=$(IMAGE_API) docker compose -f $(DEV_COMPOSE) up

down-dev:
	docker compose -f $(DEV_COMPOSE) down

logs-dev:
	docker compose -f $(DEV_COMPOSE) logs -f

test:
	docker compose -f $(DEV_COMPOSE) exec web pytest

shell:
	docker exec -it ${DOCKER_CONTAINER_NAME} /bin/bash

migrate:
	docker exec -it $(DOCKER_CONTAINER_NAME) python -m alembic upgrade head

access-db-local:
	docker exec -it $(DB_CONTAINER_NAME) mysql -u $(DB_USER) -p $(DB_NAME)

clean:
	docker compose -f $(DEV_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	docker compose -f $(PROD_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	docker images -q "api-cost-map-web*" | xargs -r docker rmi -f 2>/dev/null || true
	docker system prune -f --volumes 2>/dev/null || true
	sudo rm -f alembic/versions/* 2>/dev/null || true
	docker builder prune -f 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -type f -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

help:
	@echo ""
	@echo "🐍 API Cost MAP ($(DOCKER_TAG)) - Makefile Commands"
	@echo "──────────────────────────────────────────────"
	@echo "Development Commands:"
	@echo "  make build-dev  ➜ Build image Docker (development)"
	@echo "  make up-dev     ➜ Run local server (development)"
	@echo "  make stop       ➜ Stop local server"
	@echo "  make test       ➜ Run tests with pytest"
	@echo "  make clean      ➜ Clean local environment and containers"
	@echo ""
	@echo "Production Commands:"
	@echo "  make build-prod ➜ Build image Docker (prod)"
	@echo "  make up-prod    ➜ Start production environment with Docker Compose"
	@echo "  make down-prod  ➜ Stop production environment"
	@echo "  make logs-prod  ➜ Show production logs"
	@echo ""
