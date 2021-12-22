from django.shortcuts import render

# Create your views here.
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import FoodItems, DrinkItems


def menus(request):
    return render(request, 'menus_page.html')


class FoodMenu(generic.ListView):
    """
    Render food menus as a list of items from database
    """
    model = FoodItems
    template_name = 'food_menu.html'
    context_object_name = 'food_items'
    
    def get_queryset(self):
        # Split breakfast and dinner items up to display seperately.
        queryset = {
            'breakfast_items': FoodItems.objects.all().filter(on_menu=True, food_menu_section=0),
            'dinner_items': FoodItems.objects.all().filter(on_menu=True, food_menu_section=1)
        }
        return queryset


class DrinksMenu(generic.ListView):
    """
    Render drinks menus as a list of items from database
    """
    model = DrinkItems
    template_name = 'drinks_menu.html'
    context_object_name = 'drinks_items'

    def get_queryset(self):
        # Split drinks items up to display seperately.
        queryset = {
            'hotdrinks_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=0),
            'fruitjuices_smoothies_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=1),
            'alcohol_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=2)
        }
        return queryset