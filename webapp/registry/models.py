from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ASSET_CATEGORIES = [
    ('I', 'Industrial'),
    ('C', 'Commercial'),
    ('R', 'Residential'),
    ('A', 'Agricultural'),
]


class Asset(models.Model):
    alias = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    category = models.CharField(max_length=1, choices=ASSET_CATEGORIES)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
