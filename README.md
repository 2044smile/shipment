# shipment

## Installed

- django==4.2.11 `# stable version`
- djangorestframewwork

## Middleware

- GET /health/ `# ok`

## Feature

1. UserModel Kakao Login
2. End-point Create
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
