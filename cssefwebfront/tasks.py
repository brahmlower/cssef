from celery import task
from cssefwebfront import cssef
from cssefwebfront.settings import logger

@task()
def run_comp(compid):
	cssef.run_comp(compid)
	