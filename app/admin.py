from django.contrib import admin
from .models import Order, Delivery, Item


admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Item)
