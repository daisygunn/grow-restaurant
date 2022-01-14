from django.test import TestCase, Client
from django.urls import reverse, resolve
from menus.models import FoodItem, DrinkItem


class TestMenusViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.menus_url = reverse('menus')
        self.food_menu_url = reverse('food_menu')
        self.drink_menu_url = reverse('drinks_menu')

    def test_menus_GET(self):
        response = self.client.get(self.menus_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menus_page.html')

    def test_food_menu_GET(self):
        response = self.client.get(self.food_menu_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_menu.html')


    def test_drink_menu_GET(self):
        response = self.client.get(self.drink_menu_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'drinks_menu.html')