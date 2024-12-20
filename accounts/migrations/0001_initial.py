# Generated by Django 4.2.11 on 2024-12-04 12:31

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='데이터가 생성 된 날짜입니다.', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='데이터가 수정 된 날짜입니다.', verbose_name='수정 일시')),
                ('user_id', models.CharField(max_length=32, unique=True, verbose_name='user_id')),
                ('password', models.CharField(max_length=32, null=True, verbose_name='password')),
                ('username', models.CharField(max_length=32, null=True, verbose_name='username')),
                ('kakao_id', models.IntegerField(null=True, verbose_name='kakao_id')),
                ('kakao_nickname', models.CharField(max_length=32, null=True, verbose_name='nickname')),
                ('is_valid', models.BooleanField(default=False, verbose_name='is valid')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
