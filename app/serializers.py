from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items_details = serializers.SerializerMethodField()
    purchase_date = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Order
        fields = ['items_details', 'purchase_date']
        # fields = ['user', 'items_details', 'purchase_date']

    def get_items_details(self, obj):
        return {item.id: item.name for item in obj.items.all()}


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'