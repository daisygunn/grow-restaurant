from .models import Customer, Reservation
from django import forms
from django.conf import settings


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name', 'email', 'phone_number')


class ReservationForm(forms.ModelForm):
    requested_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMAT)
    class Meta:
        model = Reservation
        fields = ('no_of_guests', 'requested_date', 'requested_time')

        
