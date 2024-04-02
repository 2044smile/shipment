from django.db import models

from accounts.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,  # 최초 저장
        blank=True,
        null=False,
        verbose_name="생성 일시",
        help_text="데이터가 생성 된 날짜입니다."
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # 저장 될 때 마다
        blank=True,
        null=False,
        verbose_name="수정 일시",
        help_text="데이터가 수정 된 날짜입니다."
    )
    is_valid=models.BooleanField(default=False)

    class Meta:
        abstract = True


class Item(BaseModel):
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
    user=models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    order=models.OneToOneField(Order, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    status=models.CharField(max_length=16, choices=DELIVERY_STATUS, default='0')
    # departure_date=models.DateTimeField() # 배송 출발일 random
