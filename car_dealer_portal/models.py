from django.db import models
from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User


class Area(models.Model):
    pincode = models.CharField(validators = [MinLengthValidator(6), MaxLengthValidator(6)],max_length = 6,unique=True)
    city = models.CharField(max_length = 20)

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.OneToOneField(Area, on_delete=models.PROTECT)
    wallet = models.IntegerField(default = 0)

class Vehicles(models.Model):
    Status_choices=[
        ('Official','Official'),
        ('Unofficial','Unofficial'),
    ]

    car_name = models.CharField(max_length = 20)
    color = models.CharField(max_length = 10)
    dealer = models.ForeignKey(CarDealer, on_delete = models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null = True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default = True)
    description = models.CharField(max_length = 100)
    reservation_date=models.DateField(default="2024-01-01")
    driver_name = models.CharField(max_length=20, default='Unknown')
    driver_contact = models.CharField(max_length=20, default='Unknown')
    

    status= models.CharField(max_length=10,choices=Status_choices,default='Official')


