.PHONY: up down test lint schema migrations shell

# Docker Desktop ships `docker compose`; Colima + Homebrew ships `docker-compose`.
COMPOSE ?= $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo docker-compose)

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

test:
	$(COMPOSE) exec api pytest --cov --cov-report=term-missing

lint:
	$(COMPOSE) exec api sh -c "ruff check . && ruff format --check . && mypy ."
	$(COMPOSE) exec web sh -c "npm run lint && npm run typecheck"

schema:
	$(COMPOSE) exec api python manage.py spectacular --file openapi.yaml --validate
	$(COMPOSE) exec web npm run api:generate

migrations:
	$(COMPOSE) exec api python manage.py makemigrations

shell:
	$(COMPOSE) exec api python manage.py shell
