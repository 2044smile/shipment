# shipment

## Introduce

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/docker compose-8896ED?style=for-the-badge&logo=docker&logoColor=white">

- 회원 서비스 구현 완료
  - 카카오 로그인 djangorestframework-simplejwt 이용하여 액세스 토큰 관리
- 배송 서비스 구현 완료
  - docker-compose (django, rabbitmq, celery)
  - 배송 출발 ➡ Rabbitmq(broker) + Celery(worker) 비동기 300초 지연 시간 ➡ 배송 도착
- 아이템 서비스 구현 완료
- 주문 서비스 구현 완료

## Installed

- django==4.2.11 `# stable version`
- djangorestframework
- djangorestframework-simplejwt
- drf-yasg

## Docker-compose

- Django
- rabbitmq
- celery

## Middleware

- GET /health/ `# ok`

## Feature

~~1. UserModel Kakao signin, signup~~ <br>
~~2. docker-compose (django, rabbitmq, celery~~) <br>
~~3. I used Swagger(drf-yasg)~~ <br>
~~4. simplejwt using bearer JWT token~~ <br>
5. TestCode

## API
### Account
- [POST] accounts/signup
- [POST] accounts/signin
- [POST] accounts/token/verify
- [POST] accounts/token/refresh
### Deliveries
- [GET] /deliveries/ list 
- [POST] /deliveries/ create
- [GET] /deliveries/{id}/ read
- [PUT] /deliveries/{id}/ update
- [PATCH] /deliveries/{id}/ partial update
- [DELETE] /deliveries/{id}/ delete
- [GET] /deliveries/{id}/departure departure ➡ arrival
### Items
- [GET] /deliveries/ list 
- [POST] /deliveries/ create
- [GET] /deliveries/{id}/ read
- [PUT] /deliveries/{id}/ update
- [PATCH] /deliveries/{id}/ partial update
- [DELETE] /deliveries/{id}/ delete
### Orders
- [GET] /deliveries/ list 
- [POST] /deliveries/ create
- [GET] /deliveries/{id}/ read
- [PUT] /deliveries/{id}/ update
- [PATCH] /deliveries/{id}/ partial update
- [DELETE] /deliveries/{id}/ delete


## TIP

- 딕셔너리 컴프리헨션
```python
class OrderSerializer(serializers.ModelSerializer):
    items_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['user', 'items_details']

    def get_items_details(self, obj):
        return {item.id: item.name for item in obj.items.all()}
```

- get_random_string 랜덤 문자열
```python
from django.utils.crypto import get_random_string

target = get_random_string(length=16, allowed_chars="가나다라마바사thankyousomuch")
```

- Swagger details
```python
access_token = openapi.Parameter('access_token', openapi.IN_QUERY, description="Send it to me from Frontend", required=True, type=openapi.TYPE_STRING)
@swagger_auto_schema(operation_description="프론트엔드(POSTMAN) 토큰 전달", responses={200: 'Success'}, manual_parameters=[access_token])
```

- custom middleware
```python
from django.http import JsonResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health/' or request.path == '/health':
            return JsonResponse({"status": "ok"}, status=200)
        return self.get_response(request)
```

- Celery all flow
```python
# config/settings.py
INSTALLED_APPS = ['celery',]

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")
CELERY_BROKER_URL="amqp://guest:guest@rabbitmq:5672//"
# CELERY_RESULT_BACKEND = 'django-db'

# config/celery.py
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery("config")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# config/__init__.py
from .celery import app as celery_app


__all__ = ['celery_app']

# app/tasks.py
from config.celery import app

from .models import Delivery


@app.task
def process_delivery_task(delivery_id):
    instance = Delivery.objects.get(id=delivery_id)
    instance.status = "2"
    instance.is_valid = True  # 배송 완료
    instance.save()

# app/views.py
class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'], name='departure')
    def departure(self, request, pk=None):
        instance = self.get_object()
        if instance.status == '2':
            return JsonResponse({'message': f'{instance.receiver.kakao_id} 고객님의 상품은 이미 배송이 완료 되었습니다.'})
        instance.status = '1'
        instance.save()

        process_delivery_task.s(delivery_id=instance.id).apply_async(countdown=60)

        return JsonResponse({'message': f'{instance.receiver.kakao_id} 고객님의 상품 {instance.order.item.name} 배송이 출발하였습니다. the delivery service will arrive in 60 seconds'})
```

### Reference

- [POSTMAN으로 프론트엔드 역할 대체](https://rhdqors.tistory.com/39)
- [Swagger](https://drf-yasg.readthedocs.io/en/stable/custom_spec.html#the-swagger-auto-schema-decorator)

### TMI

- GOAL
  - v1
    - item, order, delivery 모델들은 Celery, Rabbitmq 비동기 작업에 집중화
  - v2
    - item, order, delivery 를 중고나라, 당근마켓과 비슷한 방향으로 모델링

- 20240813
  - accounts
    - ~~배달의 민족 처럼 카카오, 소셜 로그인을 하게 되면 username 랜덤~~
    - ~~카카오 로그인을 하고 받은 토큰은 자사 웹 회원가입/로그인 시 인증 용도로 사용~~
    - ~~자사 웹 회원가입/로그인이 되면 simplejwt 토큰으로 관리~~
  - app/order
    - ~~change ManyToMany to OneToOneField~~
      - ~~중고나라, 당근마켓 처럼 1:1 거래만 가능~~
- 20240814
  - make a config/permissions.py
  - use @property for models