from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = ['user', 'name', 'description', 'price']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    purchase_date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'item', 'purchase_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeliverySerializer(serializers.ModelSerializer):
    sender = serializers.IntegerField(read_only=True)

    class Meta:
        model = Delivery
        fields = ['order', 'sender', 'address', 'status']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user  # 토큰 사용자는 sender
        return super().create(validated_data)
