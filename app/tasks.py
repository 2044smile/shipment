import time
import random

from celery import shared_task
from config.celery import app
from datetime import timedelta
from django.utils import timezone

from .models import Delivery


def test(self, delivery_id):
    print('start', flush=True)
    instance = Delivery.objects.get(id=delivery_id)
    instance.status = "2"
    instance.save()


@app.task
def process_delivery_task(delivery_id):
    test(delivery_id=delivery_id)
    # second = random.randint(5, 10)
    # # eta = timezone.now() + timedelta(minutes=random_delivery_departure_time)
    # time.sleep(second)

    
