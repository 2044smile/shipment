# Generated by Django 4.2.11 on 2024-04-07 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('0', 'pending'), ('1', 'departure'), ('2', 'arrival')], default='0', max_length=16),
        ),
    ]