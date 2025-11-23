from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Product, Order
from decimal import Decimal

class OrderTestCase(APITestCase):

    def setUp(self):
        self.superuser_token = 'omni_pretest_superuser_token'
        self.normal_token = 'omni_pretest_token'

        self.product = Product.objects.create(
            name='iPhone 15',
            price=Decimal('29900.00')
        )

    def test_import_order_success(self):
        data = {
            'product_id': self.product.id,
            'product_amount': 2
        }
        response = self.client.post(
            '/api/import-order/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.normal_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(result['product_id'], self.product.id)
        self.assertEqual(result['product_amount'], 2)
        self.assertEqual(result['total_price'], '59800.00')

        self.assertEqual(Order.objects.count(), 1)


    def test_import_order_product_not_found(self):
        data = {
            'product_id': 99999,
            'product_amount': 2
        }
        response = self.client.post(
            '/api/import-order/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.normal_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Product not found')

    def test_import_order_invalid_amount(self):
        data = {
            'product_id': self.product.id,
            'product_amount': -5
        }
        response = self.client.post(
            '/api/import-order/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.normal_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    def test_import_order_missing_product_id(self):
        data = {'product_amount': 2}
        response = self.client.post(
            '/api/import-order/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.normal_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'product_id is required')

    def test_import_order_without_auth(self):
        data = {
            'product_id': self.product.id,
            'product_amount': 2
        }
        response = self.client.post('/api/import-order/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders_success(self):
        Order.objects.create(
            product=self.product,
            product_amount=3,
            total_price=Decimal('89700.00')
        )

        response = self.client.get(
            '/api/get-orders/',
            HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.json()
        self.assertIsInstance(orders, list)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]['product_amount'], 3)

    def test_get_orders_with_normal_token(self):
        response = self.client.get(
            '/api/get-orders/',
            HTTP_AUTHORIZATION=f'Bearer {self.normal_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders_without_auth(self):
        response = self.client.get('/api/get-orders/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)