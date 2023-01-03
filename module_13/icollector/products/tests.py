from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    def test_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('products:index')
        self.assertEqual(response.context['title'], 'Home - iCollector')


class ProductListTestCase(TestCase):
    fixtures = ['categories', 'products']

    def setUp(self) -> None:
        self.products = Product.objects.all()

    def test_list(self):
        response = self.client.get(reverse('products:products'))
        self._common_tests(response)
        self.assertEqual(list(response.context['object_list']), list(self.products[:3]))

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._common_tests(response)
        self.assertEqual(
            list(response.context['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('products:products')
        self.assertEqual(response.context['title'], 'Products - iCollector')

