# Generated by Django 4.2.11 on 2024-03-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kakao_id',
            field=models.IntegerField(default=1, max_length=32, unique=True, verbose_name='Kakao ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='kakao_nickname',
            field=models.CharField(max_length=32, unique=True, verbose_name='Kakao Nickname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, verbose_name='username'),
        ),
    ]
