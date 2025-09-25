up-bot:
	python3 -m main
makemigrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
db_raw_scripts:
	python3 -m db_manip.db_init.basic_calls
start-app:
	make migrate && make db_raw_scripts && make up-bot