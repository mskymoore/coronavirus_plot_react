import os
from celery import Celery
from celery.signals import celeryd_init


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coronavirus_plot_web.settings')

app = Celery('coronavirus_plot_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


