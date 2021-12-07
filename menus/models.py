from django.db import models

FOOD_MENU_SECTION = ((0, "Breakfast/Brunch"), (1, "Dinner"))
DRINKS_MENU_SECTION = ((0, "Hot Drinks"), (1, "Fruit juices/Soft Drinks"), (2, "Wine/Beer/Cocktails"))

# Create your models here.
class FoodItems(models.Model):
    dish_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    dietary = models.CharField(max_length=200)
    allergens = models.CharField(max_length=200)
    food_menu_section = models.IntegerField(choices=FOOD_MENU_SECTION)
    on_menu = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-on_menu']

    def __str__(self):
        return self.dish_name


class DrinkItems(models.Model):
    drink_id = models.AutoField(primary_key=True)
    drink_name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    allergens = models.CharField(max_length=200)
    drinks_menu_section = models.IntegerField(choices=DRINKS_MENU_SECTION)
    on_menu = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-on_menu']

    def __str__(self):
        return self.drink_name