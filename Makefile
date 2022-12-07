run:
	poetry run python -m service
	
alembic_up = make alembic-up

ifdef OS
	docker_up = docker compose up -d --build
	docker_down = docker compose down
else
	docker_up = sudo docker-compose up -d --build
	docker_down = sudo docker-compose down
endif

up:
	$(docker_up) 
	$(alembic_up)

down:
	$(docker_down)



test-sync:
	make renew-sync
	poetry run pytest -m my --verbosity=2 --showlocals --cov=service --cov-report html

renew:
	poetry run alembic -c alembic.ini downgrade -1
	poetry run alembic -c alembic.ini upgrade head

test:
	make renew
	poetry run pytest -m my --verbosity=2 --showlocals

async-alembic-init:
	poetry run alembic init -t async async_migrations
	poetry run alembic -c alembic.ini revision --autogenerate -m "async_initial"

alembic-up:
	poetry run alembic -c alembic.ini upgrade head

alembic-down:
	poetry run alembic -c alembic.ini downgrade -1

lint:
	poetry run isort service tests
	poetry run black service tests
	poetry run pylint service

req:
	poetry export -f requirements.txt --without-hashes --with dev --output requirements.txt

req-without-dev:
	poetry export -f requirements.txt --without-hashes --without dev --output service/requirements.txt
