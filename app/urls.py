from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'deliveries', views.DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
