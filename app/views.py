from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ItemSerializer, OrderSerializer, DeliverySerializer
from .models import Item, Order, Delivery
from app.tasks import process_delivery_task
from config.permissions import CannotPurchaseOwnProductPermission


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['GET'], name='departure')
    def departure(self, request, pk=None):
        instance = self.get_object()
        if instance.status == '2':
            return JsonResponse({'message': f'{instance.receiver.kakao_id} 고객님의 상품은 이미 배송이 완료 되었습니다.'})
        instance.status = '1'
        instance.save()

        process_delivery_task.s(delivery_id=instance.id).apply_async(countdown=60)

        return JsonResponse({'message': f'{instance.receiver.kakao_id} 고객님의 상품 {instance.order.item.name} 배송이 출발하였습니다. the delivery service will arrive in 60 seconds'})
