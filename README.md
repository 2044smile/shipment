# shipment

## Installed

- django==4.2.11 `# stable version`
- djangorestframewwork

## Middleware

- GET /health/ `# ok`

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
