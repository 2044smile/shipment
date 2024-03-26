from django.contrib import admin
from .models import User, Order, Delivery, Item


admin.site.register(User)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Item)
