# Generated by Django 4.0.3 on 2024-05-24 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer_portal', '0002_cardealer_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
