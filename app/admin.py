from django.contrib import admin
from .models import Order, Delivery, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_items', 'created_at', 'updated_at']

    def get_items(self, obj):
        return "\n".join([i.name for i in obj.items.all()])
    

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'order', 'address', 'status', 'created_at', 'updated_at']
