from django.shortcuts import render

# Create your views here.
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import FoodItems, DrinkItems


class FoodMenu(generic.ListView):
    model = FoodItems
    queryset = FoodItems.objects.filter(on_menu=True).order_by('-food_menu_section')
    template_name = 'food_menu.html'