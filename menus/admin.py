from django.contrib import admin
from .models import FoodItem, DrinkItem


# Register your models here.
@admin.register(FoodItem)
class FoodAdmin(admin.ModelAdmin):

    list_filter = ('on_menu', 'updated_on')
    list_display = ('dish_name', 'food_menu_section', 'price', 'on_menu')


@admin.register(DrinkItem)
class DrinksAdmin(admin.ModelAdmin):

    list_filter = ('on_menu', 'updated_on')
    list_display = ('drink_name', 'drinks_menu_section', 'price', 'on_menu')
