from faker import Faker

from django.db import models
from django.db.models import F, Sum


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
    description=models.TextField(null=True)
    price=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Order(BaseModel): # 주문날짜 BaseModel created_at
    # user=models.ForeignKey('User', on_delete=models.CASCADE)
    items=models.ManyToManyField(Item)

    # def save(self, *args, **kwargs):
    #     super(Order, self).save(*args, **kwargs)
    #     user = User.objects.get(id=self.user.id)
    #     user.order_set.last()
    #     import pdb;
    #     pdb.set_trace()

    # @property
    # def property_total_price(self):
    #     import pdb;
    #     pdb.set_trace()
    #     self.total_price=self.items.values().aggregate(total_price=Sum('price'))
    #     return self.total_price


class Delivery(BaseModel):
    DELIVERY_STATUS = (
        ('0', 'pending'),
        ('1', 'departure'),
        ('2', 'arrival')
    )
    order=models.OneToOneField(Order, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    status=models.CharField(max_length=16, choices=DELIVERY_STATUS)
    # departure_date=models.DateTimeField() # 배송 출발일 random

    # @property
    # def departure_date(self):
    #     fake = Faker()
    #     departure_date = self.order_set.created_at
    #     fake.date_between(start_date=self.order_set.created_at, end_date='+12h')
    #     return self.order_set.created_at
