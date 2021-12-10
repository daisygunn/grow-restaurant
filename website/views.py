from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View

from .forms import ContactForm

# Create your views here.
def index(request):

    return render(request, 'index.html')


class ContactPage(View):

    def get(self, request, *args, **kwargs):
        contact_form = ContactForm()
        template = 'contact_us.html'
        return render(request, 'contact_us.html', {'contact_form': contact_form})


    def contact_form(request):

        if request.method == 'POST':
            contact_form = ContactForm(request.POST)

            if form.is_valid():
                return render(request, 'contact_us.html', {'contact_form': contact_form})

            else:
                contact_form = ContactForm()
            
            return render(request, 'contact_us.html', {'contact_form': contact_form})