from celery import Celery

# Celery app
celery_app = Celery('worker', backend='rpc://', broker='pyamqp://')

celery_app.conf.task_routes = {
    "worker.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)
