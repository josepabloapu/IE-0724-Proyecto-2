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
            'hour_of_day',
            'day_of_week',
            'day_of_month',
            'day_of_year',
            'week_of_month',
            'week_of_year',
            'month',
            'year',
            'provider',
            'client',
            'province',
            'latitude',
            'longitude',
            
        ]
        labels = {
            'datetime': 'Datetime',
            'hour_of_day': 'Hour',
            'day_of_week': 'Day of the week',
            'day_of_month': 'Day of the month',
            'day_of_year': 'Day of the year',
            'week_of_month': 'Week of the month',
            'week_of_year': 'Week of the year',
            'month': 'Month',
            'year': 'Year',
            'provider': 'Provider',
            'client': 'Client',
            'province': 'Province',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }
        required = (
            'datetime',
            'provider',
            'client',
            'province',
            'latitude',
            'longitude',
        )
        widgets = {
            'datetime': DateTimeInput(),
            'hour_of_day': forms.HiddenInput(),
            'day_of_week': forms.HiddenInput(),
            'day_of_month': forms.HiddenInput(),
            'day_of_year': forms.HiddenInput(),
            'week_of_month': forms.HiddenInput(),
            'week_of_year': forms.HiddenInput(),
            'month': forms.HiddenInput(),
            'year': forms.HiddenInput(),
        }
