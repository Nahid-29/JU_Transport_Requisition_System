# Generated by Django 4.0.3 on 2024-05-26 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer_portal', '0006_vehicles_driver_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='driver_name',
            field=models.CharField(default='Unknown', max_length=20),
        ),
    ]