from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm


# Create your views here.
class ReservationsEnquiry(View):
    template_name = "reservations.html"

    def get(self, request, *args, **kwargs):

        customer_form = CustomerForm()
        # reservation_form = ReservationForm(initial={'email': request.user.email})
        reservation_form = ReservationForm()

#       On SUbmit
#       Check to see if there is availablity First
#       check against reservation table for number of bookings already existing for date and time, reserved and confirmed not not deleted
#       select count(*) from reservation where date = :date and time = :time and reservation =  (“confirmed”);
#         {number}

#       select count(*) from tables;
#         {max 5}

#       If number of reservation does not equal to number of rows in the seats table then
#         #allow booking
#         --Save CUstomer details to cutomer table, take the  running (primary key) id from there (store into variable)
#         --then pushreservation data into reservation table and mark reservation trigger as 1 and confirmed as 0
#         --
#       else
#         not allowed, suggest other dates
#       end if

        return render(
            request, self.template_name, 
            {'customer_form': customer_form, 'reservation_form': reservation_form}
            )


    def post(self, request, *args, **kwargs):
        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)

        if customer_form.is_valid():
            # customer_form.instance.email = request.
            customer_form.save()

            if reservation_form.is_valid():
                reservation_form.save()    

            else:
                return render(
                    request, 'reservations.html', 
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                    )  
                

        return render(
                    request, 'reservations.html', 
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                    )
