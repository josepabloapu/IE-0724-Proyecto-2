from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.
APPOINTMENT_PROVIDERS = [
    ('O1', 'Office 1'),
    ('O2', 'Office 2'),
    ('O3', 'Office 3'),
    ('O4', 'Office 4'),
    ('O5', 'Office 5'),
]

APPOINTMENT_PROVINCES = [
    ('SJ', 'San Jose'),
    ('AL', 'Alajuela'),
    ('CA', 'Cartago'),
    ('HE', 'Heredia'),
    ('GU', 'Guanacaste'),
    ('PU', 'Puntarenas'),
    ('LI', 'Limon'),
]


class Appointment(models.Model):
    datetime = models.DateTimeField(default=datetime(1990, 1, 1))
    provider = models.CharField(max_length=3, choices=APPOINTMENT_PROVIDERS)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=2, choices=APPOINTMENT_PROVINCES)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
