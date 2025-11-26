start-app:
	cd /app/celery/src && celery -A tasks.worker.tasks worker

start-beat-app:
	cd /app/celery/src && celery -A tasks.worker.tasks worker --beat