# Generated by Django 4.2.11 on 2024-03-28 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, null=True, verbose_name='username'),
        ),
    ]
