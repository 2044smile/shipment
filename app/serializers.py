from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    purchase_date = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Order
        fields = ['user', 'items', 'purchase_date']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'