from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from . import models
import json

# Create your tests here.
class InvoiceViewSetTestCase(APITestCase):
    list_url = reverse("invoices-list")
    detail_url = reverse("invoices-detail", args=[1])

    def setUp(self):
        invoice = models.Invoice.objects.create(customer_name="testing")

    def test_invoice_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_retrieve(self):
        response = self.client.get(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_invoice_create(self):
        data = {'customer_name': 'test', "invoice_details": []
        }

        response = self.client.post(self.list_url, json.dumps(data), content_type='application/json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invoice_update(self):
        data = {'id': 1, 'customer_name': 'testing', "invoice_details": [
            {
                "id": 2,
                "description": "Test description 2",
                "quantity": 12,
                "unit_price": 20.0,
                "price": 240.0
            }
        ]}
        response = self.client.patch(reverse('invoices-detail', kwargs={'pk': 1}), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)