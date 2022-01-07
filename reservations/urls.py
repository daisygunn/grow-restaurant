from reservations import views
from django.urls import path, include
from django.conf.urls import include, url

urlpatterns = [
    path('', views.ReservationsEnquiry.as_view(), name='reservations'),
    path('manage_reservations', views.ManageReservations.as_view(), name='manage_reservations'),
    path('edit_reservation/<reservation_id>', views.EditReservation.as_view(), name='edit_reservation'),
    path('delete_reservation/<reservation_id>', views.DeleteReservation.as_view(), name='delete_reservation'),
    path('edit_customer_details', views.EditCustomerDetails.as_view(), name='edit_customer_details'),
    ]