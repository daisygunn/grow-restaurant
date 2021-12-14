from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput, TimePickerInput
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm


# Create your views here.
class ReservationsEnquiry(View):
    template_name = "reservations.html"

    def get(self, request, *args, **kwargs):

        customer_form = CustomerForm()
        reservation_form = ReservationForm()

        return render(
            request, self.template_name, 
            {'customer_form': customer_form, 'reservation_form': reservation_form}
            )


    def post(self, request, *args, **kwargs):
        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)

        if customer_form.is_valid() and reservation_form.is_valid():
            # customer_form.instance.email = request.
            customer_form.save()
            reservation_form.save()
            messages.add_message(
                request, messages.SUCCESS, "Your enquiry has been sent - please note this is not approved until you receive a confirmaton email.")
           

            return render(
                    request, 'reservations.html'
                    # {'customer_form': customer_form, 'reservation_form': reservation_form}
                    )

        else:
            messages.add_message(request, messages.ERROR, "Something is not right with your form")

            return render(
                request, 'reservations.html', 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
            )  
                

        
