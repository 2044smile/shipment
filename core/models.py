from django.db import models


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
    # is_valid=models.BooleanField(default=False)

    class Meta:
        abstract = True
