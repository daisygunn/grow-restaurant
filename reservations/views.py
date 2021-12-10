from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.context_processors import csrf
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm
from bootstrap_datepicker_plus import DateTimePickerInput

# Create your views here.
class ReservationsEnquiry(View):

    def get(self, request, *args, **kwargs):
        
        template_name = "reservations.html"
        
        return render(
            request, 'reservations.html', 
            {'customer_form': CustomerForm(), 'reservation_form': ReservationForm()}
            )


    def post(self, request, *args, **kwargs):
        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)

        if customer_form.is_valid() and reservation_form.is_valid():
            
   

            return render(
                request, 'reservations.html', 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
                )