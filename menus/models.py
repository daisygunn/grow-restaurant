from django.db import models

FOOD_MENU_SECTION = ((0, "Breakfast/Brunch"), (1, "Dinner"), (2, "New item"))
DRINKS_MENU_SECTION = (
    (0, "Hot Drinks"), (1, "Fruit juices/Soft Drinks"),
    (2, "Wine/Beer/Cocktails"), (3, "New item"))


# Create your models here.
class FoodItem(models.Model):
    """
    Food items model
    """
    dish_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    dietary = models.CharField(max_length=200)
    allergens = models.CharField(max_length=200, null=True)
    food_menu_section = models.IntegerField(
        choices=FOOD_MENU_SECTION, default=2)
    on_menu = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-on_menu']

    def __str__(self):
        return self.dish_name


class DrinkItem(models.Model):
    """
    Drink items model
    """
    drink_id = models.AutoField(primary_key=True)
    drink_name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    dietary = models.CharField(max_length=200)
    allergens = models.CharField(max_length=200, null=True)
    drinks_menu_section = models.IntegerField(
        choices=DRINKS_MENU_SECTION, default=3)
    on_menu = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-on_menu']

    def __str__(self):
        return self.drink_name
