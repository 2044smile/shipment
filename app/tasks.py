from config.celery import app

from .models import Delivery


@app.task
def process_delivery_task(delivery_id):
    instance = Delivery.objects.get(id=delivery_id)
    instance.status = "2"
    instance.is_valid = True  # 배송 완료
    instance.save()
