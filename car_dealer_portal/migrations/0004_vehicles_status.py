# Generated by Django 4.0.3 on 2024-05-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer_portal', '0003_alter_vehicles_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='status',
            field=models.CharField(choices=[('Official', 'Official'), ('Unofficial', 'Unofficial')], default='Official', max_length=10),
        ),
    ]
