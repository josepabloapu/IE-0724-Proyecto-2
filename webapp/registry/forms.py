from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Appointment

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'datetime',
            'provider',
            'client',
            'province',
            'latitude',
            'longitude',
            
        ]
        labels = {
            'datetime': 'Datetime',
            'provider': 'Provider',
            'client': 'Client',
            'province': 'Province',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }
        widgets = {
            'datetime': DateTimeInput(),
        }
