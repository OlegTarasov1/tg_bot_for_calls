start-app:
	cd /app/celery/src && celery -A tasks.worker.tasks worker --loglevel="INFO"

start-beat-app:
	cd /app/celery/src && celery -A tasks.beat.tasks beat --loglevel="INFO"