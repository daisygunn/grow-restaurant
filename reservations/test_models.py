from django.test import TestCase
from reservations.models import Reservation, Table, Customer


class TestReservationsModels(TestCase):

    def setUp(self):
        self.table = Table(table_id=1, table_name='Table 1', max_no_people=4)
        self.customer = Customer(
            customer_id=12, full_name='Test 123', email='test123@gmail.com')
        self.reservation = Reservation(
            reservation_id=32,
            table=self.table,
            customer=self.customer,
            no_of_guests=4, requested_date='2022-01-23',
            requested_time='12:00', status='pending')

    def test_create_table(self):
        self.assertEqual(self.table.table_id, 1)
        self.assertEquals(self.table.table_name, 'Table 1')
        self.assertEquals(self.table.max_no_people, 4)

    def test_create_customer(self):
        self.assertEqual(self.customer.customer_id, 12)
        self.assertEquals(self.customer.full_name, 'Test 123')
        self.assertEquals(self.customer.email, 'test123@gmail.com')

    def test_create_reservation(self):
        self.assertEqual(self.reservation.reservation_id, 32)
        self.assertEquals(self.reservation.table, self.table)
        self.assertEquals(self.reservation.customer, self.customer)
        self.assertEquals(self.reservation.no_of_guests, 4)
        self.assertEquals(self.reservation.requested_date, '2022-01-23')
        self.assertEquals(self.reservation.requested_time, '12:00')
        self.assertEquals(self.reservation.status, 'pending')

    def test_customer_on_delete_cascade_works(self):
        customer = self.customer
        customer.delete()

        reservations = len(Reservation.objects.all())

        self.assertEquals(reservations, 0)

    def test_table_on_delete_cascade_works(self):
        table = self.table
        table.delete()

        reservations = len(Reservation.objects.all())

        self.assertEquals(reservations, 0)
