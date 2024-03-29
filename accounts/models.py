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
    user_id = models.CharField(  # admin 유저를 위해 만든 user_id OAuth 로 카카오 로그인 시 kakao_id 의 값이 user_id 로 복사된다.
        verbose_name='user_id',
        max_length=32,
        unique=True
    )
    password = models.CharField(  # admin 유저를 위해 만든 패스워드
        verbose_name='password',
        max_length=32,
        null=True
    )
    username = models.CharField(  # 랜덤으로 생성되는 username
        verbose_name='username',
        max_length=32,
        null=True
    )
    kakao_id = models.IntegerField(  # 카카오 로그인 시 사용자에게 발급되면 kakao_id 고유키
        verbose_name='kakao_id',
        null=True
    )
    kakao_nickname = models.CharField(  # 카카오 사용자가 설정한 nickname
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
        if self.is_staff:  # admin 유저의 경우 is_staff 가 True 일 것이기에 return user_id 하지만 일반 유저의 경우 return kakao_id
            return self.user_id
        else:
            return str(self.kakao_id)
