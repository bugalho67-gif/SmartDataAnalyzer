build:
	docker compose build

run:
	docker compose up

stop:
	docker compose down

restart:
	docker compose down
	docker compose up --build

logs:
	docker compose logs -f

clean:
	docker system prune -f
