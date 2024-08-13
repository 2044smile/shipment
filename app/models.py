from django.db import models

from accounts.models import User
from core.models import BaseModel


class Item(BaseModel):
    user=models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name=models.CharField(max_length=64)
    description=models.TextField(blank=True)
    price=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Order(BaseModel): # 주문날짜 BaseModel created_at
    user=models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    items=models.ManyToManyField(Item)

    def get_items(self, obj):
        return "\n".join([i.name for i in obj.itmes.all()])
    
    def __str__(self):
        return "\n".join([i.name for i in self.items.all()])

class Delivery(BaseModel):
    DELIVERY_STATUS = (
        ('0', 'pending'),
        ('1', 'departure'),
        ('2', 'arrival')
    )
    sender = models.ForeignKey('accounts.User', related_name='sent_deliveries', on_delete=models.CASCADE)
    receiver = models.ForeignKey('accounts.User', related_name='received_deliveries', on_delete=models.CASCADE)
    order=models.OneToOneField(Order, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    status=models.CharField(max_length=16, choices=DELIVERY_STATUS, default='0')
