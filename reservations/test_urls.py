from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from reservations.views import ReservationsEnquiry, ManageReservations, EditReservation, DeleteReservation


# Create your tests here
class TestReservationsUrls(SimpleTestCase):
    def test_reservations_url_is_resolved(self):
        url = reverse('reservations')
        self.assertEquals(resolve(url).func.view_class, ReservationsEnquiry)

    def test_manage_reservations_url_is_resolved(self):
        url = reverse('manage_reservations')
        self.assertEquals(resolve(url).func.view_class, ManageReservations)

    def test_edit_reservations_url_is_resolved(self):
        url = reverse('edit_reservation', args=['reservation_id'])
        self.assertEquals(resolve(url).func.view_class, EditReservation)

    def test_delete_reservation_url_is_resolved(self):
        url = reverse('delete_reservation', args=['reservation_id'])
        self.assertEquals(resolve(url).func.view_class, DeleteReservation)
