.PHONY: test lint infra-up infra-down

test:
	pytest -q

lint:
	ruff check .

infra-up:
	docker compose up -d postgres redis

infra-down:
	docker compose down

.PHONY: eda-image inference-up inference-down inference-smoke eda-loop
eda-image:
	docker build -t llm4security-eda:phase1 containers/eda

inference-up:
	docker compose --env-file .env -f deploy/inference/compose.yaml up -d

inference-down:
	docker compose --env-file .env -f deploy/inference/compose.yaml down

inference-smoke:
	uv run --env-file .env llm4security-inference-smoke

eda-loop:
	uv run --extra eda --env-file .env llm4security-eda-loop $(SOURCES) --top $(TOP)
