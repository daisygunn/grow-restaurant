from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from .models import Table, Customer, Reservation
from .forms import CustomerForm, ReservationForm
import logging

logger = logging.getLogger(__name__)


def retreive_customer_info(reservation_form, customer_form):
    # Retreive information from forms 
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
    no_tables_booked = len(Reservation.objects.filter(
        requested_time=customer_requested_time, requested_date=customer_requested_date, status="confirmed"))
                        
    # Return number of tables
    return no_tables_booked


def get_customer_instance(request, User):
    """
    Returns customer instance if User is logged in """
    customer_email = request.user.email
    customer = Customer.objects.filter(email=customer_email).first()

    return customer

def get_tables_info():
    """
    Retrieves the number of tables in the 
    table model
    """
    max_tables = Table.objects.all().count

    return max_tables

# Create your views here.
class ReservationsEnquiry(View):
    template_name = "reservations.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            customer_form = CustomerForm(instance=customer)
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
                {'customer_form': customer_form, 'reservation_form': reservation_form})

        
        # return render(request, self.template_name)
        

    def post(self, request, User=User, *args, **kwargs):

        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)
        if customer_form.is_valid() and reservation_form.is_valid():
            # Retreive information from forms 
            customer_requested_time, customer_requested_date, customer_requested_guests, customer_name, customer_phone_number = retreive_customer_info(reservation_form, customer_form)

            # Check to see how many bookings exist at that time/date
            tables_booked = check_availabilty(customer_requested_time, customer_requested_date)
            max_tables = get_tables_info

            # Compare number of bookings to number of tables available
            if tables_booked == max_tables:
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
                current_customer = get_customer_instance(request, User)
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
                return render(
                    request, 'reservations.html',
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )
        
        else:
            messages.add_message(
                request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")
      
        return render(
                    request, 'reservations.html',
                    {'customer_form': customer_form, 'reservation_form': reservation_form}
                )


def retrieve_reservations(self, request, User):
    customer_email = request.user.email
    if len(Customer.objects.filter(email=customer_email)) != 0:
        current_customer = Customer.objects.get(email=customer_email)
        current_customer_id = current_customer.pk
        logger.warning(f"user = {customer_email}") 

        get_reservations = Reservation.objects.filter(customer_name=current_customer_id).values().order_by('requested_date')
        logger.warning(f"{get_reservations}")

        if len(get_reservations) == 0:
            # if no reservations
            logger.warning(f"No existing reservations.") 
            return 1
        else:
            return get_reservations
    else:
        # if user is not present in customer model
        logger.warning(f"No user in customer model") 
        return 1


class ManageReservations(View):
    # View for user to manage any existing reservations
    def get(self, request, User=User, *args, **kwargs):        
        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            model = Reservation
            current_reservations = retrieve_reservations(self, request, User)
            # If the user has no reservations
            if current_reservations == 0:
                messages.add_message(request, messages.WARNING, "Ooops, you've not got any existing reservations. You can make reservations here.")
                url = reverse('reservations')
                return HttpResponseRedirect(url)
            # If the user does not exist in the customer model 
            elif current_reservations == 1:
                messages.add_message(request, messages.WARNING, "Ooops, you've never made a reservation enquiry. You can make reservations here.")
                url = reverse('reservations')
                return HttpResponseRedirect(url)
                
            else:
                return render(
                    request, 'manage_reservations.html', 
                    {'reservations': current_reservations,
                    'customer': customer})

        else:
            messages.add_message(
                request, messages.ERROR, "You must be logged in to manage your reservations.")

        return render(request, 'manage_reservations.html')


class EditReservation(View):
    # View for user to be able to edit their existing reservations
    def get(self, request, reservation_id, User=User, *args, **kwargs):
        # Get reservation object based on id
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        customer = get_customer_instance(request, User)
        logger.warning(reservation)
        logger.warning(customer)

        # return both forms with the existing information
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
        customer = get_customer_instance(request, User)
        reservation_id = reservation_id
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        logger.warning(f"{reservation}")
        reservation_form = ReservationForm(data=request.POST, instance=reservation)
        customer_form = CustomerForm(instance=customer)

        if reservation_form.is_valid():
            # get the information from the form 
            customer_requested_time = reservation_form.cleaned_data['requested_time']
            customer_requested_date = reservation_form.cleaned_data['requested_date']
            # Check the amount of tables already booked at that date and time
            tables_booked = check_availabilty(customer_requested_time, customer_requested_date)
            # Get total number of tables in restaurant
            max_tables = get_tables_info

            # Compare number of bookings to number of tables available
            if tables_booked == max_tables:
                # if the amount of tables already booked = the max tables then reject the reservation.
                messages.add_message(
                    request, messages.ERROR, f"Unfortunately we are fully booked at {customer_requested_time} on {customer_requested_date}")

            else:
                # Update the existing reservation with the form data.
                reservation.reservation_id = reservation_id
                reservation.requested_time = customer_requested_time
                reservation.requested_date = customer_requested_date
                reservation.requested_guests = reservation_form.cleaned_data['no_of_guests']
                # Change status to pending as the admin needs to approve
                reservation.status = 'pending'
                reservation_form.save(commit=False)
                reservation_form.save()
                messages.add_message(request, messages.SUCCESS, "Your reservation has now been updated.")
                # Retreive new list of reservations to display
                current_reservations = retrieve_reservations(self, request, User)

                # Return user to manage reservations page
                return render(request, 'manage_reservations.html', {'reservations': current_reservations})
                
        else:
            messages.add_message(request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")
            
        return render(request, 'edit_reservation.html', {'reservation_form': reservation_form, 'customer_form': customer_form, 'reservation': reservation, 'customer': customer, })

class DeleteReservation(View):
    # View for user to delete reservations
    def get(self, request, reservation_id, User=User, *args, **kwargs):
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
        # customer_email = request.user.email
        # customer = Customer.objects.filter(email=customer_email).first()
        customer = get_customer_instance(request, User)

        return render(request, 'delete_reservation.html',
        {'customer': customer,
        'reservation': reservation,
        'reservation_id': reservation_id 
        })

    
    def post(self, request, reservation_id, User=User, *args, **kwargs):
        customer = get_customer_instance(request, User)
        # get reservation from database
        reservation_id = reservation_id
        reservation = Reservation.objects.get(pk=reservation_id)
        logger.warning(f"{reservation}")
        # Delete the reservation
        reservation.delete()
        messages.add_message(request, messages.SUCCESS, "Your reservation has now been deleted.")
        # Get updated list of reservations
        current_reservations = retrieve_reservations(self, request, User)
        # Return user to manage reservations page
        return render(
                    request, 'manage_reservations.html', 
                    {'reservations': current_reservations,
                    'customer': customer})


class EditCustomerDetails(View):
    # View for user to be able to edit their information
    def get(self, request, User=User, *args, **kwargs):
        # Get customer object based on user
        customer = get_customer_instance(request, User)

        logger.warning(customer)

        # return both forms with the existing information
        customer_form = CustomerForm(instance=customer)

        return render(request, 'edit_customer_details.html', 
        {'customer_form': customer_form,
        'customer': customer,
        })

    
    def post(self, request, User=User, *args, **kwargs):
        customer = get_customer_instance(request, User)

        customer_form = CustomerForm(data=request.POST, instance=customer)
        
        if customer_form.is_valid():
            if customer_form.has_changed():
                # get the information from the form
                customer_full_name = customer_form.cleaned_data['full_name']
                customer_email = customer_form.cleaned_data['email']
                customer_phone_number = customer_form.cleaned_data['phone_number']
            
                customer_form.save(commit=False)
                customer.full_name = customer_full_name
                customer.phone_number = customer_phone_number
                customer_form.save()
                messages.add_message(request, messages.SUCCESS, "Your details have now been updated.")
                return render(request, 'edit_customer_details.html', 
                {'customer_form': customer_form,
                'customer': customer,
                })

            else:
                messages.add_message(request, messages.WARNING, "No information has changed.")
                return render(request, 'edit_customer_details.html', 
                {'customer_form': customer_form,
                'customer': customer,
                })
        else:
            messages.add_message(request, messages.ERROR, "Something is not right with your form - please make sure your email address & phone number are entered in the correct format.")
            
        return render(request, 'edit_customer_details.html', 
        {'customer_form': customer_form,
        'customer': customer,
        })