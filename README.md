# shipment

## Installed

- django==4.2.11 `# stable version`
- djangorestframewwork
- drf-yasg

## Middleware

- GET /health/ `# ok`

## Feature

~~1. UserModel Kakao Login~~ used POSTMAND and Wrote a code
~~2. End-point Create~~ used Swagger(drf-yasg)
3. /admin 페이지 상품 관리

## FLOW

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