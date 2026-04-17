# Makefile API Cost Map
PROJECT_NAME = API Cost Map
DOCKER_IMAGE_NAME = api-cost-map-web
DOCKER_CONTAINER_NAME = api-cost-map
PORT = 8000
DOCKER_TAG ?= dev
DEV = docker compose -f docker-compose.dev.yaml
PROD = docker compose -f docker-compose.prod.yaml
DE = docker exec -it
DB_CONTAINER_NAME = postgres-server
DB_PORT = 5432
DB_NAME = costdb
DB_USER = admin
DB_PASS = pass

run-dev:
	$(DEV) up --build

down-dev:
	$(DEV) down

logs-dev:
	$(DEV) logs -f

test:
	$(DEV) exec web pytest

run-prod:
	$(PROD) up --build -d

down-prod:
	$(PROD) down

logs-prod:
	$(PROD) logs -f

restart-web:
	$(PROD) restart web

restart-nginx:
	$(PROD) restart nginx

shell:
	$(DE) $(DOCKER_CONTAINER_NAME) /bin/bash

migration:
	$(DE) $(DOCKER_CONTAINER_NAME) python -m alembic revision --autogenerate -m "$(m)"

migrate:
	$(DE) $(DOCKER_CONTAINER_NAME) alembic upgrade head

current:
	$(DE) $(DOCKER_CONTAINER_NAME) alembic current

history:
	$(DE) $(DOCKER_CONTAINER_NAME) alembic history

access-db-local:
	$(DE) $(DB_CONTAINER_NAME) psql -U $(DB_USER) -d $(DB_NAME)

clean:
	$(DEV) down -v --remove-orphans --rmi local 2>/dev/null || true
	$(PROD) down -v --remove-orphans --rmi local 2>/dev/null || true
	find . \( -name "__pycache__" -o -name "*.pyc" \) -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov .ruff_cache 2>/dev/null || true

clean-all: clean
	docker rmi -f $$( $(DEV) config --images ) 2>/dev/null || true
	docker rmi -f $$( $(PROD) config --images ) 2>/dev/null || true

format:
	$(DEV) exec web ruff format app

lint:
	$(DEV) exec web pylint app

help:
	@echo ""
	@echo "$(PROJECT_NAME) ($(DOCKER_TAG)) - Makefile Commands"
	@echo "──────────────────────────────────────────────"
	@echo ""
	@echo "Development:"
	@echo "  make run-dev         Start dev environment"
	@echo "  make down-dev        Stop dev environment"
	@echo "  make logs-dev        Show dev logs"
	@echo "  make test            Run tests"
	@echo ""
	@echo "Production:"
	@echo "  make run-prod        Start prod environment"
	@echo "  make down-prod       Stop prod environment"
	@echo "  make logs-prod       Show prod logs"
	@echo "  make restart-web     Restart web service"
	@echo "  make restart-nginx   Restart nginx"
	@echo ""
	@echo "Utilities:"
	@echo "  make shell           Access container shell"
	@echo "  make migration       Create migration"
	@echo "  make migrate         Apply migrations"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Clean containers and cache"
	@echo "  make clean-all       Full cleanup"
