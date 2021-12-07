from django.shortcuts import render
from django.views import generic, View

# Create your views here.
def index(request):

    return render(request, 'index.html')

def menus(request):

    return render(request, 'menus.html')