from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    """Create and return a tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

def create_tag(user, name):
    """Create and return a new tag"""
    return Tag.objects.create(user=user, name=name)

class PublicTagsAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        create_tag(self.user, 'Vegan')
        create_tag(self.user, 'Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to user"""
        other_user = create_user(email='other@example.com', password='testpass123')
        create_tag(other_user, 'Vegan')
        create_tag(self.user, 'Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.filter(user=self.user)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """Test updating a tag"""
        tag = create_tag(self.user, 'Dessert')

        payload = {'name': 'After Dinner'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag"""
        tag = create_tag(self.user, 'Dessert')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        exist = Tag.objects.filter(id=tag.id).exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)
