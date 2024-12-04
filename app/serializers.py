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
    sender = serializers.PrimaryKeyRelatedField(read_only=True)  # read_only=True 설정한 이유는 토큰(request.user) 로 사용자 정보를 가져와서 sender로 저장하기 위함

    class Meta:
        model = Delivery
        fields = ['order', 'sender', 'address', 'status']

    def create(self, validated_data):
        # validated_data 에 직접 추가하지 않고, 인스턴스를 생성할 때 sender를 지정
        delivery = Delivery.objects.create(sender=self.context['request'].user, **validated_data)

        return delivery
