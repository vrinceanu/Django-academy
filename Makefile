.PHONY: up down test lint schema migrations shell

up:
	docker compose up --build

down:
	docker compose down

test:
	docker compose exec api pytest --cov --cov-report=term-missing

lint:
	docker compose exec api sh -c "ruff check . && ruff format --check . && mypy ."
	docker compose exec web sh -c "npm run lint && npm run typecheck"

schema:
	docker compose exec api python manage.py spectacular --file openapi.yaml --validate
	docker compose exec web npm run api:generate

migrations:
	docker compose exec api python manage.py makemigrations

shell:
	docker compose exec api python manage.py shell
