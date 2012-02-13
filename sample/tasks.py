from celery.decorators import task
from pprint import pprint

@task()
def add(x, y):
	pprint("executing task")
	return x + y