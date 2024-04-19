from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="id")
    user_id = serializers.IntegerField(source="user.id")
    purchase_date = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'items', 'purchase_date']


class DeliverySerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="id")
    user_id = serializers.IntegerField(source="user.id")

    class Meta:
        model = Delivery
        fields = ['order_id', 'user_id', 'address', 'status']