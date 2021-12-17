from django.shortcuts import render, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput, TimePickerInput
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class ReservationsEnquiry(View):
    template_name = "reservations.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer_form = CustomerForm(initial={'full_name': request.user.first_name + " " + request.user.last_name, 'email': request.user.email})
            reservation_form = ReservationForm()
            return render(
                request, self.template_name, 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
                )
        else:
            messages.add_message(
                        request, messages.ERROR, "You must be logged in to make a reservation.")
                        
        logger.warning("Get request")
        return render(
                request, self.template_name)
        

    
    def post(self, request, *args, **kwargs):

        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)
        max_tables = Table.objects.all().count()

        logger.warning(f"Maximum number of tables: {max_tables}")
        
        # You must be logged in to make in a reservation enquiry
        @login_required
        def send_reservation(self, customer_form, reservation_form, max_tables, request):
            if customer_form.is_valid() and reservation_form.is_valid():
                
                customer_requested_time = reservation_form.cleaned_data['requested_time']
                customer_requested_date = reservation_form.cleaned_data['requested_date']

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
                            request, messages.SUCCESS, f"Your enquiry for {customer_requested_time} on {customer_requested_date} has been sent - please note this is not approved until you receive a confirmaton email.")
                    
                    return render(request, 'reservations.html')

            else:

                messages.add_message(request, messages.ERROR, "Something is not right with your form")

                return render(
                    request, 'reservations.html', 
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )  
       
        return render(
                    request, 'reservations.html',
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )  
        
