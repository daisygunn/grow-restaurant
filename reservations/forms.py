from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput, TimePickerInput
from .models import Customer, Reservation
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name', 'email', 'phone_number')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('no_of_guests', 'requested_date', 'requested_time')
        widgets = {
            'requested_date': DatePickerInput(options={
                    # "format": "DD/MM/YYYY", # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }),
        }

        
       
