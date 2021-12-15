from django.shortcuts import render, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput, TimePickerInput
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm
import logging

logger = logging.getLogger(__name__)

# Put the logging info within your django view


# Create your views here.
class ReservationsEnquiry(View):
    template_name = "reservations.html"

    def get(self, request, *args, **kwargs):

        customer_form = CustomerForm()
        reservation_form = ReservationForm()

        logger.warning("Get request")
        return render(
            request, self.template_name, 
            {'customer_form': customer_form, 'reservation_form': reservation_form}
            )


    def post(self, request, *args, **kwargs):

        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)
        max_tables = Table.objects.all().count()
        # max_tables = 1

        logger.warning(f"Maximum number of tables: {max_tables}")
        
        
        if customer_form.is_valid() and reservation_form.is_valid():
            
            customer_requested_time = reservation_form.cleaned_data['requested_time']
            customer_requested_date = reservation_form.cleaned_data['requested_date']

            # def get_no_tables_booked(customer_requested_date, customer_requested_time):

            logger.warning(f"{customer_requested_time}, {customer_requested_date}")

            queryset = len(Reservation.objects.filter(
                requested_time=customer_requested_time, requested_date=customer_requested_date, status="confirmed"))
                    
            logger.warning(f"{queryset}")
            print(queryset)

            if queryset == max_tables:

                messages.add_message(
                    request, messages.ERROR, f"Unfortunately we are fully booked at {customer_requested_time} on {customer_requested_date}")

                return render(
                request, 'reservations.html', 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
                )            
            
            else:
                customer_form.save()
                reservation_form.save()

                messages.add_message(
                        request, messages.SUCCESS, "Your enquiry has been sent - please note this is not approved until you receive a confirmaton email.")
                
                return render(request, 'reservations.html')

        else:

            messages.add_message(request, messages.ERROR, "Something is not right with your form")

            return render(
                request, 'reservations.html', 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
            )  
                

        
