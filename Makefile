# Makefile API Cost Map
DOCKER_IMAGE_NAME = api-cost-map-web
DOCKER_CONTAINER_NAME = api-cost-map
PORT = 8000
DOCKER_TAG=1.0.0
IMAGE_API = $(DOCKER_IMAGE_NAME)-api:$(DOCKER_TAG)
COMPOSE = docker compose
DEV_COMPOSE = docker-compose.dev.yaml
PROD_COMPOSE = docker-compose.prod.yaml
DB_CONTAINER_NAME = mysql-server
DB_PORT = 3306
DB_NAME = costdb
DB_USER = admin
DB_PASS = pass


build-dev:
	chmod +x entrypoint.sh
	IMAGE_API=$(IMAGE_API) $(COMPOSE) -f $(DEV_COMPOSE) build

run-dev: build-dev
	IMAGE_API=$(IMAGE_API) $(COMPOSE) -f $(DEV_COMPOSE) up

down-dev:
	$(COMPOSE) -f $(DEV_COMPOSE) down

logs-dev:
	$(COMPOSE) -f $(DEV_COMPOSE) logs -f

test:
	$(COMPOSE) -f $(DEV_COMPOSE) exec web pytest

build-prod:
	$(COMPOSE) -f $(PROD_COMPOSE) build

run-prod: build-prod
	$(COMPOSE) -f $(PROD_COMPOSE) up

restart-web:
	$(COMPOSE) -f $(PROD_COMPOSE) restart web

restart-nginx:
	$(COMPOSE) -f $(PROD_COMPOSE) restart nginx

shell:
	docker exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

migrate:
	docker exec -it $(DOCKER_CONTAINER_NAME) alembic upgrade head

migrate:
	docker exec -it $(DOCKER_CONTAINER_NAME) alembic upgrade head

current:
	docker exec -it $(DOCKER_CONTAINER_NAME) alembic current

history:
	docker exec -it $(DOCKER_CONTAINER_NAME) alembic history

access-db-local:
	docker exec -it $(DB_CONTAINER_NAME) mysql -u $(DB_USER) -p $(DB_NAME)

clean:
	docker compose -f $(DEV_COMPOSE) down -v --remove-orphans --rmi local 2>/dev/null || true
	docker compose -f $(PROD_COMPOSE) down -v --remove-orphans --rmi local 2>/dev/null || true
	find . \( -name "__pycache__" -o -name "*.pyc" \) -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

clean-all: clean
	docker rmi -f $$(docker compose -f $(DEV_COMPOSE) config --images) 2>/dev/null || true
	docker rmi -f $$(docker compose -f $(PROD_COMPOSE) config --images) 2>/dev/null || true

format:
	$(COMPOSE) -f $(DEV_COMPOSE) exec web ruff format app

lint:
	$(COMPOSE) -f $(DEV_COMPOSE) exec web pylint app


help:
	@echo ""
	@echo "API Cost MAP ($(DOCKER_TAG)) - Makefile Commands"
	@echo "──────────────────────────────────────────────"
	@echo "Development Commands:"
	@echo "  make build-dev  ➜ Build image Docker (development)"
	@echo "  make run-dev    ➜ Run local server (development)"
	@echo "  make stop       ➜ Stop local server"
	@echo "  make test       ➜ Run tests with pytest"
	@echo "  make clean      ➜ Clean local environment and containers"
	@echo "  make format     ➜ Format code with ruff"
	@echo "  make lint       ➜ Lint code with pylint"
	@echo ""
	@echo "Production Commands:"
	@echo "  make build-prod ➜ Build image Docker (prod)"
	@echo "  make run-prod   ➜ Start production environment with Docker Compose"
	@echo "  make down-prod  ➜ Stop production environment"
	@echo "  make logs-prod  ➜ Show production logs"
	@echo "  make restart-web ➜ Restart web service"
	@echo "  make restart-nginx ➜ Restart nginx service"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean-all  ➜ Clean all local environment and containers"
	@echo ""
