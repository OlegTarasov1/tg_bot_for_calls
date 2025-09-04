up-bot:
	python3 -m main
makemigrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
start-app:
	make migrate && make up-bot