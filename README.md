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

## Middleware

- GET /health/ `# ok`

## Feature

~~1. UserModel Kakao signin, signup~~<br>
~~2. I used Swagger(drf-yasg)~~ <br>
~~3. simplejwt using bearer JWT token~~ <br>
4. TestCode

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

### Reference

- [POSTMAN으로 프론트엔드 역할 대체](https://rhdqors.tistory.com/39)
- [Swagger](https://drf-yasg.readthedocs.io/en/stable/custom_spec.html#the-swagger-auto-schema-decorator)