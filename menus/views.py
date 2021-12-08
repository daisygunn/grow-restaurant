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
    queryset = DrinkItems.objects.filter(on_menu=True).order_by('drinks_menu_section')
    template_name = 'drinks_menu.html'