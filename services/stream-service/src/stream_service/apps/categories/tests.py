from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        response = self.client.post(
            "/api/categories/",
            {
                "name": "Gaming",
                "slug": "gaming",
                "description": "Gaming streams",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
