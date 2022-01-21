from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import FoodItem, DrinkItem


def menus(request):
    return render(request, 'menus_page.html')


class FoodMenu(generic.ListView):
    """
    Render food menus as a list of items from database
    """
    model = FoodItem
    template_name = 'food_menu.html'
    context_object_name = 'food_items'

    def get_queryset(self):
        # Split breakfast and dinner items up to display seperately.
        queryset = {
            'breakfast_items': FoodItem.objects.all().filter(
                on_menu=True, food_menu_section=0),
            'dinner_items': FoodItem.objects.all().filter(
                on_menu=True, food_menu_section=1)
        }
        return queryset


class DrinksMenu(generic.ListView):
    """
    Render drinks menus as a list of items from database
    """
    model = DrinkItem
    template_name = 'drinks_menu.html'
    context_object_name = 'drinks_items'

    def get_queryset(self):
        # Split drinks items up to display seperately.
        queryset = {
            'hotdrinks_items': DrinkItem.objects.all().filter(
                on_menu=True, drinks_menu_section=0),
            'fruitjuices_smoothies_items': DrinkItem.objects.all().filter(
                on_menu=True, drinks_menu_section=1),
            'alcohol_items': DrinkItem.objects.all().filter(
                on_menu=True, drinks_menu_section=2)
        }
        return queryset
