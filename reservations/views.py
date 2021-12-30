from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from bootstrap_datepicker_plus import DatePickerInput
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm
import logging

logger = logging.getLogger(__name__)

# Retreive number of tables in restaurant
max_tables = Table.objects.all().count()


def retreive_customer_info(reservation_form, customer_form):
    # Retreive information from form 
    customer_requested_time = reservation_form.cleaned_data['requested_time']
    customer_requested_date = reservation_form.cleaned_data['requested_date']
    customer_requested_guests = reservation_form.cleaned_data['no_of_guests']
    customer_name = customer_form.cleaned_data['full_name']
    customer_phone_number = customer_form.cleaned_data['phone_number']

    logger.warning(f"{customer_requested_time}, {customer_requested_date}")
    
    return customer_requested_time, customer_requested_date, customer_requested_guests, customer_name, customer_phone_number

def check_availabilty(customer_requested_time, customer_requested_date):
    # check availability against Reservation model using customer input 
    logger.warning(f"{customer_requested_time}, {customer_requested_date}")

            # Check to see how many bookings exist at that time/date
    queryset = len(Reservation.objects.filter(
        requested_time=customer_requested_time, requested_date=customer_requested_date, status="confirmed"))
                        
    logger.warning(f"{queryset}")
    return queryset

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

        logger.warning(f"Maximum number of tables: {max_tables}")
       
        if customer_form.is_valid() and reservation_form.is_valid():

            # Retreive information from form 
            # customer_requested_time = reservation_form.cleaned_data['requested_time']
            # customer_requested_date = reservation_form.cleaned_data['requested_date']
            # customer_requested_guests = reservation_form.cleaned_data['no_of_guests']
            # customer_name = customer_form.cleaned_data['full_name']

            # logger.warning(f"{customer_requested_time}, {customer_requested_date}")
            customer_requested_time, customer_requested_date, customer_requested_guests, customer_name, customer_phone_number = retreive_customer_info(reservation_form, customer_form)

            # Check to see how many bookings exist at that time/date
            # table_availability = len(Reservation.objects.filter(
            #     requested_time=customer_requested_time, requested_date=customer_requested_date, status="confirmed"))
                        
            # logger.warning(f"{table_availability}")
            table_availability = check_availabilty(customer_requested_time, customer_requested_date)

            # Compare number of bookings to number of tables available
            if table_availability == max_tables:
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
                else:
                    customer_form.save()

                # Retreive customer information pass to reservation model
                current_customer = Customer.objects.get(email=customer_email)
                current_customer_id = current_customer.pk
                customer = Customer.objects.get(customer_id=current_customer_id)
                logger.warning(f"Customer ID is: {current_customer_id}")
                logger.warning(f"{customer}")
                reservation = reservation_form.save(commit=False)
                reservation.customer_name = customer
                reservation_form.save()

                messages.add_message(
                        request, messages.SUCCESS, f"Thank you {customer_name}, your enquiry for {customer_requested_guests} people at {customer_requested_time} on {customer_requested_date} has been sent.")
                
                # Return blank forms so the same enquiry isn't sent twice.
                return HttpResponseRedirect(reverse('reservations'))
        
        else:
            messages.add_message(
                request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")
      
        return render(
                    request, 'reservations.html',
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )

def retrieve_reservations(self, request, User):
    customer_email = request.user.email
    current_customer = Customer.objects.get(email=customer_email)
    current_customer_id = current_customer.pk
    logger.warning(f"user = {customer_email}") 

    get_reservations = Reservation.objects.filter(customer_name=current_customer_id).values().order_by('requested_date')
    logger.warning(f"{get_reservations}")

    return get_reservations

class ManageReservations(View):
    # View for user to manage any existing reservations
    def get(self, request, User=User, *args, **kwargs):        
        if request.user.is_authenticated:
            customer_email = request.user.email
            customer = Customer.objects.filter(email=customer_email).first()
            model = Reservation
            current_reservations = retrieve_reservations(self, request, User)
            paginate_by = 4
            return render(
                request, 'manage_reservations.html', 
                {'reservations': current_reservations,
                'customer': customer})

        else:
            messages.add_message(
                request, messages.ERROR, "You must be logged in to manage your reservations.")

        return render(request, 'manage_reservations.html')


class EditReservation(View):
    
    def get(self, request, reservation_id, User=User, *args, **kwargs):
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        # reservation = Reservation.objects.filter(reservation_id=reservation_id).first()
        customer_email = request.user.email
        customer = Customer.objects.filter(email=customer_email).first()
    
        logger.warning(reservation)
        logger.warning(customer)
        
        customer_form = CustomerForm(instance=customer)
        reservation_form = ReservationForm(instance=reservation)

        return render(request, 'edit_reservation.html', 
        {'customer_form': customer_form,
        'customer': customer,
        'reservation_form': reservation_form,
        'reservation': reservation,
        'reservation_id': reservation_id 
        })

    def post(self, request, reservation_id, User=User, *args, **kwargs):
        customer_email = request.user.email
        customer = Customer.objects.filter(email=customer_email).first()
        reservation_id = reservation_id
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        logger.warning(f"{reservation}")
        reservation_form = ReservationForm(data=request.POST, instance=reservation)
        customer_form = CustomerForm(instance=customer)

        if reservation_form.is_valid():

            customer_requested_time = reservation_form.cleaned_data['requested_time']
            customer_requested_date = reservation_form.cleaned_data['requested_date']

            table_availability = check_availabilty(customer_requested_time, customer_requested_date)

            # Compare number of bookings to number of tables available
            if table_availability == max_tables:
                messages.add_message(
                    request, messages.ERROR, f"Unfortunately we are fully booked at {customer_requested_time} on {customer_requested_date}")

            else:
                reservation.reservation_id = reservation_id
                reservation.requested_time = customer_requested_time
                reservation.requested_date = customer_requested_date
                reservation.requested_guests = reservation_form.cleaned_data['no_of_guests']
                reservation.status = 'pending'
                reservation_form.save(commit=False)
                reservation_form.save()
                messages.add_message(request, messages.SUCCESS, "Your reservation has now been updated.")
                current_reservations = retrieve_reservations(self, request, User)
                return render(request, 'manage_reservations.html', {'reservations': current_reservations})
                # return ReservationsEnquiry(request)
        else:
            messages.add_message(request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")
            
        return render(request, 'edit_reservation.html', {'reservation_form': reservation_form, 'customer_form': customer_form, 'reservation': reservation, 'customer': customer, })

class DeleteReservation(View):
    def get(self, request, reservation_id, User=User, *args, **kwargs):
        # reservation_id = reservation_id
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        # reservation = Reservation.objects.filter(reservation_id=reservation_id).first()
        customer_email = request.user.email
        customer = Customer.objects.filter(email=customer_email).first()
        
        return render(request, 'delete_reservation.html',
        {'customer': customer,
        'reservation': reservation,
        'reservation_id': reservation_id 
        })

    def post(self, request, reservation_id, User=User, *args, **kwargs):
        customer_email = request.user.email
        customer = Customer.objects.filter(email=customer_email).first()
        reservation_id = reservation_id
        reservation = Reservation.objects.get(pk=reservation_id)
        logger.warning(f"{reservation}")
        reservation.delete()
        current_reservations = retrieve_reservations(self, request, User)
        return render(
                request, 'manage_reservations.html', 
                {'reservations': current_reservations,
                'customer': customer})
        