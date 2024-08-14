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
    item=models.OneToOneField(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.item.name

class Delivery(BaseModel):
    DELIVERY_STATUS = (
        ('0', 'pending'),
        ('1', 'departure'),
        ('2', 'arrival')
    )
    # sender = models.ForeignKey('accounts.User', related_name='sent_deliveries', on_delete=models.CASCADE)
    # receiver = models.ForeignKey('accounts.User', related_name='received_deliveries', on_delete=models.CASCADE)
    """
    득도 receiver 필드가 필요하지 않다. 왜냐하면 Order 모델에는 `user` 구매자와 `item` 이 있으며 `Item` 모델에는 `user(판매자)`가 있습니다. 즉, 이미 `Order` 와 `Item` 을 통해 관계가 설정되어 있기 때문입니다.
    그리하여 order.item.user 를 통해 판매자를 참조할 수 있습니다. 데이터 구조가 간결해지고 중복된 정보가 사라집니다.

    @property
    def receiver(self):
        return self.order.user
    """
    order=models.OneToOneField(Order, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    status=models.CharField(max_length=16, choices=DELIVERY_STATUS, default='0')

    @property
    def sender(self):
        return self.order.item.user  # 판매한 사람(판매자)을 반환

    @property
    def receiver(self):
        return self.order.user  # 주문한 사람(구매자)을 반환
