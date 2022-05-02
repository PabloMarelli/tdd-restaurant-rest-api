from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_tag(user, name='Main course'):
    """
    Create and return tag
    """
    
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """
    Create and return recipe
    """
    
    return Ingredient.objects.create(user=user, name=name)


def detail_url(recipe_id):
    """
    Returns recipe detail url
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    """
    Create and return recipe
    """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)
    
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """
    Test recipes public API
    """
    
    def setUp(self):
        self.client = APIClient()
        
    def test_required_auth(self):
        """
        Test required authentication
        """
        res = self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test recipes private API
    """
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testarudo.com',
            'pass123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_retrieve_recipes(self):
        """
        Test recipe retrieve
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
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
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
        
    
    def test_view_recipe_detail(self):
        """
        Test view recipe details
        """