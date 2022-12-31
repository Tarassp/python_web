from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class IndexViewTestCase(TestCase):
    def test_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('products:index')
        self.assertEqual(response.context['title'], 'Home - iCollector')

