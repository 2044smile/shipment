from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from app.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username):
        if not username:
            raise ValueError('must have an username')
        
        user = self.model(
            username=self.normalize_email(username=username)
        )

        user.save(using=self._db)
        return user
    
    def create_superuser(self, username):
        user = self.create_user(
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        verbose_name='username',
        max_length=32,
        null=True
    )
    kakao_id = models.IntegerField(
        verbose_name='Kakao ID',
        unique=True
    )
    kakao_nickname = models.CharField(
        verbose_name='Kakao Nickname',
        max_length=32
    )
    is_valid = models.BooleanField(
        verbose_name='is valid',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='is active',
        default=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'kakao_id'

    def __str__(self):
        return self.kakao_nickname
