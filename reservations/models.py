from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.full_name


class Tables(models.Model):
    table_id = models.AutoField(primary_key=True)
    min_no_people = models.IntegerField()
    max_no_people = models.IntegerField()

    def __str__(self):
        return self.table_id


class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    guests_choices = ((1, "1 person"), (2, "2 people"), (3, "3 people"),
     (4, "4 people"), (5, "5 people"), (6, "6 people"), (7, "7 people"), 
     (8, "8 people"), (9, "9 people"), (10, "10 people"))
    no_of_guests = models.IntegerField(choices=guests_choices, default=1)
    requested_time = models.DateTimeField()
    status_choices = ((0, "pending"), (0, "confirmed"))
    status = models.CharField(
        max_length=10, choices=status_choices, default=0)

    def __str__(self):
        return self.reservation_id