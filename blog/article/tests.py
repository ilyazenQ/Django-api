import requests
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.
class ArticleApiTestCase(APITestCase):
    def test_get(self):
        response = requests.get("http://127.0.0.1:8000/api/v1/articles/")
        print(response)