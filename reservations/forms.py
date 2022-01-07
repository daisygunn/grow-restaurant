from .models import Customer, Reservation
from django import forms
from django.conf import settings
from phonenumber_field.formfields import PhoneNumberField


class CustomerForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': ('Please enter in +44 format')}))

    class Meta:
        model = Customer
        fields = ('full_name', 'email', 'phone_number')


class ReservationForm(forms.ModelForm):
    requested_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMAT)

    class Meta:
        model = Reservation
        fields = ('no_of_guests', 'requested_date', 'requested_time')
