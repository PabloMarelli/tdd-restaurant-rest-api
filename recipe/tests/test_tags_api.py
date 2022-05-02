from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """
    Test Tags public API 
    """

    def setUp(self):
        self.client = APIClient()
        
    def test_login_requiered(self):
        """
        Tests that login is requiered to obtain tags
        """

        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        

class PrivateTagsApiTests(TestCase):
    """
    Test Tags private API 
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testarudo.com',
            'pass123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        """
        Test tag retrieve
        """
        Tag.objects.create(user=self.user, name='Meat')
        Tag.objects.create(user=self.user, name='Banana')
        
        res = self.client.get(TAGS_URL)
        
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        """
        Test that retrieved tags belong to users
        """
        user2 = get_user_model().objects.create_user(
            'test@test.com',
            'pass123456',
        )
        Tag.objects.create(user=user2, name='Raspberry')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        
        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
    
    def test_create_tag_successful(self):
        """
        Test create new tag
        """
        
        payload = {'name': 'Simple'}
        self.client.post(TAGS_URL, payload)
        
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_tag_invalid(self):
        """
        Test create tag with invalid payload
        """
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        