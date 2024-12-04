from .models import *
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'user', 'name', 'description', 'price']

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
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'sender', 'receiver', 'address', 'status']

    def get_sender(self, obj):
        return obj.sender.id if obj.sender else None  # 사용자 ID 반환

    def get_receiver(self, obj):
        return obj.receiver.id if obj.receiver else None  # 사용자 ID 반환

    def create(self, validated_data):
        # Order 정보를 통해 자동으로 sender/receiver 관계를 유추
        return Delivery.objects.create(**validated_data)