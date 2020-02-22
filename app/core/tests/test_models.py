from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='user@example.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful."""
        email = 'mikkyfred@yahoo.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'testpass123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'teststs')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'mikkyfred@yahoo.com', 'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag str representation"""
        tag = models.Tag.objects.create(user=sample_user(), name='Vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient str representation"""
        ingredient = models.Ingredient.objects.create(
            name='Cucumber', user=sample_user())

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test that we can create a recipe object and successfully retrieve it as a string.
        Test the recipe str representation
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(), title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_tag_content(self):
        """Test that a user can successfully create a recipe object and retrieve its content.
        Test that the content 
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(), title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(f'{recipe.user.email}', 'user@example.com')
        self.assertEqual(recipe.time_minutes, 5)
        self.assertEqual(recipe.price, 5.00)
