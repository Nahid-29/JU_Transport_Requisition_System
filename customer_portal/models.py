from django.db import models
from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from car_dealer_portal.models import *


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

class Orders(models.Model):
    Status_choices=[
        ('Official','Official'),
        ('Unofficial','Unofficial'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)
    reservation_date=models.DateField(default="2024-01-01")
    status= models.CharField(max_length=10,choices=Status_choices,default='Official')
    cl = models.CharField(max_length=20, default='Unknown')
    mob = models.CharField(max_length=20, default='Unknown')
    em = models.CharField(max_length=20, default='Unknown')






