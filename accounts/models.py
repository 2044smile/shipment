from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from app.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('must have an username')
        
        user = self.model(
            email=self.normalize_email(username=username)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    kakao_id = models.IntegerField(
        verbose_name='Kakao ID',
        max_length=32,
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=32,
    )
    kakao_nickname = models.CharField(
        verbose_name='Kakao Nickname',
        max_length=32,
        unique=True
    )

    is_active = models.BooleanField(
        verbose_name='is active',
        default=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'kakao_nickname'
