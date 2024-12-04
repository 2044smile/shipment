# Generated by Django 4.2.11 on 2024-12-04 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='데이터가 생성 된 날짜입니다.', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='데이터가 수정 된 날짜입니다.', verbose_name='수정 일시')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='데이터가 생성 된 날짜입니다.', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='데이터가 수정 된 날짜입니다.', verbose_name='수정 일시')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='데이터가 생성 된 날짜입니다.', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='데이터가 수정 된 날짜입니다.', verbose_name='수정 일시')),
                ('address', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('0', 'pending'), ('1', 'departure'), ('2', 'arrival')], default='0', max_length=16)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
