import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library_Service.settings")

app = Celery("Library_Service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["notifications"])

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")