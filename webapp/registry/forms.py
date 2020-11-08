from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Asset


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'alias',
            'province',
            'category',
            'latitude',
            'longitude',
            'owner',
        ]
        labels = {
            'alias': 'Alias',
            'province': 'Province',
            'category': 'Category',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'owner': 'Owner',
        }
