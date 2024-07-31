"""
Test for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_ingredient(user, name):
     """Create and return a new ingredient"""
     return Ingredient.objects.create(user=user, name=name)


class PublicIngredientAPITest(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
            """Test auth is required for retrieving ingredients"""
            res = self.client.get(INGREDIENT_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients"""
