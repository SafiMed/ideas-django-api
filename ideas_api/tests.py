from django.test import TestCase

from ideas_api.models import User
from ideas_api.models import Idea

# Create your tests here.


class UserTest(TestCase):
    """User model test."""

    @classmethod
    def setUpTestData(cls):
        """User object will be used by all next test methods."""
        
        User.objects.create(email='safi@gmail.com', name='safi')

    def test_get_full_name_and_get_short_name(self):
        """The get_full_name & get_short_name functions test."""

        print("---------- Testing equality of names ----------")

        user=User.objects.get(id=1)
        self.assertEqual(user.get_full_name(), 'safi')
        self.assertEqual(user.get_short_name(), 'safi')
    
    def test_str(self):
        """The str function test."""

        print("---------- Testing two emails are equals ----------")

        user=User.objects.get(id=1)
        self.assertEqual(str(user), 'safi@gmail.com')

    def test_boolean_input_value(self):
        """The boolean variables test."""

        print("---------- Testing boolean variables ----------")

        user=User.objects.get(id=1)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)


class IdeaTest(TestCase):
    """Idea model test."""

    def test_str(self):
        """The str function test."""

        print("---------- Two ideas are equals ----------")

        idea = Idea(idea_text='My Idea Test')
        self.assertEqual(str(idea), 'My Idea Test')

