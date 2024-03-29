from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from app.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, password):
        if not user_id:
            raise ValueError('must have an user_id')
        
        user = self.model(
            user_id=user_id
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    user_id = models.CharField(
        verbose_name='user_id',
        max_length=32,
        unique=True
    )
    password = models.CharField(
        verbose_name='password',
        max_length=32,
        null=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=32,
        null=True
    )
    kakao_id = models.IntegerField(
        verbose_name='kakao_id',
        null=True
    )
    kakao_nickname = models.CharField(
        verbose_name='nickname',
        max_length=32,
        null=True
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
    USERNAME_FIELD = 'user_id'

    def __str__(self):
        if self.is_staff == True:
            return self.user_id
        else:
            return self.kakao_id
