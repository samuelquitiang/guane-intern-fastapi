from time import sleep
from celery import current_task
from .cel_app import celery_app

import sys
sys.path.append(r"C:\Users\samue\Dropbox\Proyectos\Guane\app_dogs/app")


# Celery worker with sleep
# I didnt understand all this optional and had some troubles with the connection with windows
@celery_app.task(acks_late=True)
def test_celery(dog: str) -> str:
    sleep(11)
    return f"test task return {dog}"
