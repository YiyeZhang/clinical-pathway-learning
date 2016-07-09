from celery import Celery
celery = Celery('tasks',backend='redis://localhost:6379/0', broker = 'redis://localhost:6379/0')

@celery.task
def add(x,y):
  return x+y
