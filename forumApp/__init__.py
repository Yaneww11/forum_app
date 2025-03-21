from .celery import app as celery_app

# In which app celery listen for async task
__all__ = ('posts',)