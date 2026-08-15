.PHONY: dev test coverage lint format build up deploy down logs

dev:
	streamlit run app.py

test:
	pytest tests/ -v

coverage:
	pytest tests/ -v --cov=src --cov=security --cov=ai --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

build:
	docker compose build app

up:
	docker compose up --build

deploy:
	docker compose --profile production up --build -d

down:
	docker compose --profile production down

logs:
	docker compose logs -f app nginx
