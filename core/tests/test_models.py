from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@test.com', password='pass123456'):
    """
    Creates sample user for testing
    """
    
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    
    def test_create_user_with_email_successful(self):
        """ 
        Test to create user with email successfully 
        """

        email = 'test@mail.com'
        password = 'pass123456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ 
        Email test for custom user 
        """
               
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(
            email,
            'pass123456'
        )
        
        self.assertEqual(user.email, email.lower())
        
    def test_new_user_invalid_email(self):
        """ 
        New user invalid email 
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123456')
    
    def test_create_new_superuser(self):
        """ 
        Test created superuser 
        """
        
        email = 'test@mail.com'
        password = 'pass123456'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_tag_str(self):
        """
        Test tag as text string
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Meat',
        )
        
        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        """
        Test ingredient as text string
        """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Banana',
        )
        
        self.assertEqual(str(ingredient), ingredient.name)
        
    def test_recipe_str(self):
        """
        Test recipe as text string
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00,
        )
        
        self.assertEqual(str(recipe), recipe.title)
        
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        Test that image saves in the right place
        """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)