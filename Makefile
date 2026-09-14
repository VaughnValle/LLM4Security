.PHONY: test lint infra-up infra-down

test:
	pytest -q

lint:
	ruff check .

infra-up:
	docker compose up -d postgres redis

infra-down:
	docker compose down
