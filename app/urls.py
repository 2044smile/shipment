from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'deliveries', views.DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('deliveries/', views.DeliveryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('deliveries/<int:pk>/', views.DeliveryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('deliveries/<int:pk>/departure/', views.DeliveryViewSet.as_view({'get': 'departure'})),  # 여기에 추가
]
