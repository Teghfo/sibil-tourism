from celery import shared_task
import time

@shared_task
def hello_task(name):
    return f"hello celery to {name}"


@shared_task(name="summation")
def summation(a, b):
    time.sleep(10)
    return a + b
