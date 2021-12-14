from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phone_field.models
import datetime

status_choices = (("pending", "pending"), ("confirmed", "confirmed"))

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.full_name


class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=10, default="New table", unique=True)
    max_no_people = models.IntegerField()

    def __str__(self):
        return self.table_name


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    # email = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_email")
    guests_choices = ((1, "1 person"), (2, "2 people"), (3, "3 people"), (4, "4 people"))
    no_of_guests = models.IntegerField(choices=guests_choices, default=1)
    requested_date = models.DateField(default=datetime.date.today)
    requested_time = models.TimeField(default='')
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="table_booked", null=True)
    status = models.CharField(
        max_length=10, choices=status_choices, default="pending")

    def __str__(self):
        return str(self.reservation_id)