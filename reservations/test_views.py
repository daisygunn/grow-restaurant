from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import Customer, Table, Reservation
from django.contrib.auth.models import User


class TestReservationsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='project.test@test.com',
            email='project.test@test.com', password='12345')
        login = self.client.login(
            username='project.test@test.com',
            email='project.test@test.com', password='12345')
        self.reservations_url = reverse('reservations')
        self.manage_reservations_url = reverse('manage_reservations')

        self.table = Table.objects.create(
            table_id=5,
            table_name='Table 5',
            max_no_people=4
        )

        self.customer = Customer.objects.create(
            customer_id=1,
            full_name='Project Test',
            email='project.test@test.com',
            phone_number='+447980987654'
        )

        self.reservation = Reservation.objects.create(
            reservation_id=35,
            customer_name=self.customer,
            no_of_guests=4,
            requested_date='2022-01-20',
            requested_time='12:00',
            table_id=self.table,
            status='pending'
        )

        self.edit_reservations_url = reverse('edit_reservation', args=[35])
        self.delete_reservations_url = reverse('delete_reservation', args=[35])
        self.edit_customer_details_url = reverse('edit_customer_details')

    def test_reservation_GET(self):
        response = self.client.get(self.reservations_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')

    def test_manage_reservation_GET(self):
        if self.user.is_authenticated:
            response = self.client.get(self.manage_reservations_url)

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'manage_reservations.html')
        else:
            failureException

    def test_delete_reservation_GET(self):
        response = self.client.get(self.delete_reservations_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_reservation.html')

    def test_edit_reservation_GET(self):
        response = self.client.get(self.edit_reservations_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_reservation.html')

    def test_reservation_POST_adds_new_customer_and_reservation(self):
        table = self.table

        customer = Customer.objects.create(
            customer_id=3,
            full_name='Project Test123',
            email='project.test123@test.com',
            phone_number='+447980987654'
        )

        customer.save()

        reservation = Reservation.objects.create(
            reservation_id=36,
            customer_name=customer,
            no_of_guests=4,
            requested_date='2022-01-29',
            requested_time='12:00',
            table_id=table,
            status='pending'
        )

        reservation.save()

        response = self.client.post(self.reservations_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Reservation.objects.all()), 2)
        self.assertEquals(len(Customer.objects.all()), 2)

    def test_edit_reservation_POST_updates_model(self):
        customer = self.customer
        reservation = self.reservation

        updated_date = '2022-04-01'

        reservation.requested_date = updated_date

        reservation.save()

        self.assertEquals(self.reservation.requested_date, '2022-04-11')
