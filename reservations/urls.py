from reservations import views
from django.urls import path, include
from django.conf.urls import include, url

urlpatterns = [
    path('', views.ReservationsEnquiry.as_view(), name='reservations'),
    path('manage_reservations', views.ManageReservations.as_view(), name='manage_reservations'),
    ]