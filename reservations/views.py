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
            customer_form = CustomerForm()
            reservation_form = ReservationForm()
            return render(
                request, self.template_name, 
                {'customer_form': customer_form, 'reservation_form': reservation_form}
                )
        logger.warning("Get request")
        return render(request, self.template_name)
        

    def post(self, request, User=User, *args, **kwargs):

        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)

        # Retreive number of tables in restaurant
        max_tables = Table.objects.all().count()

        logger.warning(f"Maximum number of tables: {max_tables}")
       
        if customer_form.is_valid() and reservation_form.is_valid():

            # Retreive information from form 
            customer_requested_time = reservation_form.cleaned_data['requested_time']
            customer_requested_date = reservation_form.cleaned_data['requested_date']
            customer_requested_guests = reservation_form.cleaned_data['no_of_guests']
            customer_name = customer_form.cleaned_data['full_name']

            logger.warning(f"{customer_requested_time}, {customer_requested_date}")

            # Check to see how many bookings exist at that time/date
            queryset = len(Reservation.objects.filter(
                requested_time=customer_requested_time, requested_date=customer_requested_date, status="confirmed"))
                        
            logger.warning(f"{queryset}")
            print(queryset)

            # Compare number of bookings to number of tables available
            if queryset == max_tables:
                messages.add_message(
                    request, messages.ERROR, f"Unfortunately we are fully booked at {customer_requested_time} on {customer_requested_date}")

                return render(request, 'reservations.html', 
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                    )            
                
            else:
                customer_email = customer_form.cleaned_data['email']
                customer_query = len(Customer.objects.filter(email=customer_email))

                # Prevent duplicate 'customers' being added to database
                if customer_query > 0:
                    logger.warning("customer exists")
                    pass
                else:
                    customer_form.save()

                # Retreive customer information pass to reservation model
                current_customer = Customer.objects.get(email=customer_email)
                current_customer_id = current_customer.pk
                customer = Customer.objects.get(customer_id=current_customer_id)
                logger.warning(f"Customer ID is: {current_customer_id}")
                logger.warning(f"{customer}")
                reservation = reservation_form.save(commit=False)
                reservation.customer_id = customer
                reservation_form.save()

                messages.add_message(
                        request, messages.SUCCESS, f"Thank you {customer_name}, your enquiry for {customer_requested_guests} people at {customer_requested_time} on {customer_requested_date} has been sent.")
                
                # Return blank forms so the same enquiry isn't sent twice.
                # customer_form = CustomerForm()
                # reservation_form = ReservationForm()
                return HttpResponseRedirect(reverse('reservations'))
                # return render(request, 'reservations.html', {'customer_form': customer_form, 'reservation_form': reservation_form})

        else:

            messages.add_message(
                request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")

            return render(
                request, 'reservations.html',
                {'customer_form': customer_form, 'reservation_form': reservation_form}
                )
      
        return render(
                    request, 'reservations.html',
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )

