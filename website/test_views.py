from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core import mail


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.contact_page_url = reverse('contact_us')

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_contact_page_GET(self):
        response = self.client.get(self.contact_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us.html')

    def test_contact_page_POST_sends_email(self):
        response = self.client.post(self.contact_page_url)

        mail.send_mail('Subject here', 'Here is the message.',
                       'from@example.com', ['to@example.com'],
                       fail_silently=False)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
