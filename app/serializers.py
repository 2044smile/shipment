from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)
    purchase_date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Order
        fields = ['order', 'user', 'items', 'purchase_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeliverySerializer(serializers.ModelSerializer):
    sender = serializers.IntegerField(read_only=True)

    class Meta:
        model = Delivery
        fields = ['order', 'sender', 'receiver', 'address', 'status']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user  # 토큰 사용자는 sender
        return super().create(validated_data)
