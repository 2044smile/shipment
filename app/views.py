from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from config.permissions import IsAdminOrReadOnly

from .serializers import *
from app.tasks import process_delivery_task


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['GET'], name='departure')
    def departure(self, request, pk=None):
        instance = self.get_object()
        instance.status = '1'
        instance.save()

        process_delivery_task.s(delivery_id=instance.id).apply_async(countdown=300)

        return JsonResponse({'message': f'{instance.id} 고객님 배송이 출발하였습니다. 300 초 후 도착합니다.'})