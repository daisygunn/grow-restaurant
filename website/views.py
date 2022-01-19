from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from reservations.models import Customer


# Create your views here.
def index(request):
    """ Return homepage """
    return render(request, 'index.html')


def send_message(request, contact_form):
    """ Function to send email after contact form submitted """
    customer_name = contact_form.cleaned_data['name']
    email_from = contact_form.cleaned_data['email']
    subject = (f'Message from {customer_name}, {email_from}')
    message = contact_form.cleaned_data['message']
    recipient_list = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, email_from, recipient_list)


def get_customer_instance(request, User):
    """ Returns customer instance if User is logged in """
    customer_email = request.user.email
    customer = Customer.objects.filter(email=customer_email).first()

    return customer


class ContactPage(View):
    """ Contact page - for a user to send a contact form """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)

            if customer is None:
                # If 'customer' does not exist return blank string & user email
                customer_name = ""
                customer_email = request.user.email
            else:
                # Return full name & customer email
                customer_name = customer.full_name
                customer_email = customer.email

            # if user is logged in pre-populate the fields
            contact_form = ContactForm(
                initial={'name': customer_name,  'email': customer_email})
        else:
            contact_form = ContactForm()

        return render(
            request, 'contact_us.html', {'contact_form': contact_form})

    def post(self, request, User=User, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Send email to website owner
            send_message(request, contact_form)
            # Return blank form so the same message isn't posted twice.
            contact_form = ContactForm()
            messages.add_message(
                request, messages.SUCCESS,
                "Thank you for contacting us, one of our staff will be in"
                "touch shortly. <br>For anything urgent please call on"
                "02076841002.")
            return render(
                request, 'contact_us.html', {'contact_form': contact_form})

        else:
            contact_form = ContactForm(request.POST)
            messages.add_message(
                request, messages.ERROR,
                "Something is not right with your form - please make sure your"
                "email address is entered in the correct format.")

        return render(
            request, 'contact_us.html', {'contact_form': contact_form})


def error_404(request, exception):
    """ 404 error page """
    return render(request, '404.html', status=404)


def error_500(request):
    """ 500 error page """
    return render(request, '500.html', status=500)
