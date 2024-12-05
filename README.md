# shipment

## [Introduce](https://newbiecs.tistory.com/427)

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
    instance.status = "2" # 배송 완료
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

## 시나리오

### 1. 카카오 로그인 프론트엔드 & 회원 정보 
![alt text](image.png)
1. Postman - Authorization Client ID, Callback URL, ... 설정 후 - `Get New Access Token`
2. 카카오 로그인창 - 회원가입/로그인 - `카카오 토큰 발급`
3. 카카오 토큰으로 `회원정보 확인 가능`

### 2. 회원가입/로그인 백엔드
![alt text](image-1.png)
1. 카카오 토큰으로 `회원가입/로그인` 토큰 발급 access_token
2. access_token 으로 shipment 서비스 이용 가능
3. Swagger - Authorize - Bearer eyJhbGciOiJIUzI1NiIsI...

### 3. 아이템(제품) 생성 POST /items/
1. 토큰과 함께 판매할 아이템을 생성
```json
{
    "id": 2,
    "user": 1,
    "name": "반포자이",
    "description": "",
    "price": 20000000000
}
```

### 4. 아이템(리스트) - GET /items/
1. 토큰으로 다른 사용자도 판매 등록한 아이템 조회
```json
[
    {
        "id": 1,
        "user": 2,
        "name": "리더스빌",
        "description": "",
        "price": 175000000
    },
    {
        "id": 2,
        "user": 1,
        "name": "반포자이",
        "description": "",
        "price": 20000000000
    }
]
```

### 5. 아이템 주문 - /orders/
1. 상대방의 아이템 ID 를 입력
```json
{
    "user":2,
    "item":1,
    "purchase_date":"2024-12-04T12:47:40.641913Z"
}
```

### 6. 배송 서비스 접수 - POST /deliveries/
1. 토큰으로 API 를 이용하는 사람은 판매자
2. order 정보에 판매자, 구매자 정보가 존재
```json
{
  "order": 1,
  "address": "서초구 반포동",
  "status": "0"  // pending
}
// response
{
  "id": 3,
  "order": 1,
  "sender": 1,
  "receiver": 2,
  "address": "서초구 반동",
  "status": "0"
}
```

### 7. 배송 서비스 출발/도착 - GET /deliveries/{id}/departure/
1. Delivery ID 입력
```json
{
    "id": 3
}
// response
{
  "message": "3408007879 고객님의 상품 반포자이 배송이 출발하였습니다. the delivery service will arrive in 60 seconds"
}
```
![alt text](image-2.png)