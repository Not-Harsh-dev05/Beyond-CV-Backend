.PHONY: build up down migrate test lint train-model seed-demo logs

build:
	docker compose build
up:
	docker compose up --build
down:
	docker compose down
migrate:
	docker compose run --rm migrate
test:
	python -m pytest
lint:
	ruff check apps config
	black --check apps config
train-model:
	python manage.py train_pedigree_model --data-path=$(DATA_PATH)
seed-demo:
	python manage.py seed_demo_data
logs:
	docker compose logs -f
