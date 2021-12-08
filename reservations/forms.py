from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Customer, Reservations
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name', 'email', 'phone_number')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ('no_of_guests', 'requested_time')
        widgets = {
            'requested_time':DateTimePickerInput()
        }
       
