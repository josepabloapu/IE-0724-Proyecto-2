from django import forms
from .models import Asset
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):
    pass
    '''class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']'''

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
            #'createdAt',
            #'updatedAt',
        ]
        labels = {
            'alias': 'Alias',
            'province': 'Provicia',
            'category': 'Categoria',
            'latitude': 'Latitud',
            'longitude': 'longitud',
            'owner': 'Dueño',
            #'createdAt': 'Creaciòn',
            #'updatedAt': 'Actualizada',
        }
