from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Tables, Customer, Reservations
from .forms import CustomerForm, ReservationForm


# Create your views here.
class ReservationsEnquiry(View):

    def get(self, request, *args, **kwargs):
        
        template_name = "reservations.html"
        
        return render(
            request, 'reservations.html', 
            {'customer_form': CustomerForm(), 'reservation_form': ReservationForm()},
            )


    def post(self, request, *args, **kwargs):
        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(request.POST)

        return render(
            request, 'reservations.html', 
            {'customer_form': customer_form, 'reservation_form': reservation_form},
            )