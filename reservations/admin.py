from django.contrib import admin
from .models import Customer, Table, Reservation

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email', 'phone_number')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'table_name', 'max_no_people')


@admin.register(Reservation)
class ReservationsAdmim(admin.ModelAdmin):
    list_filter = ('no_of_guests', 'status', 'table_id')
    list_display = ('reservation_id', 'customer_id', )