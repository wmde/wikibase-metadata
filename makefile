up:
	docker compose -f docker-compose.yaml -f docker-compose.local.yaml up --build -d

down:
	docker compose -f docker-compose.yaml -f docker-compose.local.yaml down
