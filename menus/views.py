from django.shortcuts import render

# Create your views here.
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import FoodItems, DrinkItems


def menus(request):
    return render(request, 'menus_page.html')

class FoodMenu(generic.ListView):
    model = FoodItems
    template_name = 'food_menu.html'
    context_object_name = 'food_items'
    
    def get_queryset(self):
        queryset = {
            'breakfast_items': FoodItems.objects.all().filter(on_menu=True, food_menu_section=0),
            'dinner_items': FoodItems.objects.all().filter(on_menu=True, food_menu_section=1)
        }
        return queryset


class DrinksMenu(generic.ListView):
    model = DrinkItems
    template_name = 'drinks_menu.html'
    context_object_name = 'drinks_items'

    def get_queryset(self):
        queryset = {
            'hotdrinks_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=0),
            'fruitjuices_smoothies_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=1),
            'alcohol_items': DrinkItems.objects.all().filter(on_menu=True, drinks_menu_section=2)
        }
        return queryset