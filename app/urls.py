from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'menu', views.ItemViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'delivery', views.DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
