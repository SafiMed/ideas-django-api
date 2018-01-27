import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from ideas_api.models import User
from ideas_api.models import Idea
from ideas_api.serializers import IdeaSerializer

# Create your tests here.


class UserTest(TestCase):
    """User model test."""

    def setUp(self):
        """User object will be used by all next test methods."""
        
        self.user = User.objects.create(email='safi@gmail.com', name='safi', password='med')

    def test_get_full_name_and_get_short_name(self):
        """The get_full_name & get_short_name functions test."""

        self.assertEqual(self.user.get_full_name(), 'safi')
        self.assertEqual(self.user.get_short_name(), 'safi')
    
    def test_str(self):
        """The str function test."""

        self.assertEqual(str(self.user), 'safi@gmail.com')

    def test_boolean_input_value(self):
        """The boolean variables test."""

        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)


class IdeaTest(TestCase):
    """Idea model test."""

    def test_str(self):
        """The str function test."""

        idea = Idea(idea_text='My Idea Test')
        self.assertEqual(str(idea), 'My Idea Test')


class IdeaTestCase(APITestCase):
    """Idea API test."""

    def setUp(self):
        """Create an authenticated user. Create an idea. Define urls."""
        self.user = User.objects.create(email='safi@gmail.com', name='safi', password='med')
        self.idea = Idea.objects.create(user_id=self.user, idea_text="This is my first idea test!")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication(self.token.key)

        self.url_list = reverse('api:ideas-list', kwargs={'id': self.user.pk})
        self.url_detail = reverse("api:ideas-detail", kwargs={'id': self.user.pk, 'pk': self.idea.pk})

        self.other_user = User.objects.create(email='other_user@gmail.com', name='other', password='user')
        self.other_user_token = Token.objects.create(user=self.other_user)

    def api_authentication(self, token_key):
        """Set a token key in headers used on all requests."""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_get_idea_list(self):
        """Test getting idea list."""

        response = self.client.get(self.url_list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_idea_object(self):
        """Test getting idea object."""

        response = self.client.get(self.url_detail)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        # Inspecting the data that was created in the setUp function
        idea_serializer_data = IdeaSerializer(instance=self.idea).data
        self.assertEqual(idea_serializer_data, response.data)
        
    def test_idea_object_create_authorization(self):
        """Test POST HTTP Method with other user token."""

        self.api_authentication("")

        data = {}
        response = self.client.post(self.url_list, data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_idea_object_create(self):
        """Test POST HTTP method with the logged in user."""

        data = {'idea_text': 'Test Create idea!'}
        response = self.client.post(self.url_list, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_idea_object_update_authorization(self):
        """Test PUT/PATCH HTTP methods with other user token."""

        self.api_authentication(self.other_user_token.key)

        # HTTP METHOD : PUT
        response = self.client.put(self.url_detail, {"idea_text": "Update my first idea test!"})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        # HTTP METHOD : PATCH
        response = self.client.patch(self.url_detail, {"idea_text": "Partial update my first idea test!"})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_idea_object_update(self):
        """Test PUT HTTP method with the logged in user."""

        response = self.client.put(self.url_detail, {"idea_text": "Update my first idea test!"})
        idea = Idea.objects.get(id=self.idea.id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("idea_text"), idea.idea_text)

    def test_idea_object_partial_update(self):
        """Test PATCH HTTP method with the logged in user."""

        response = self.client.patch(self.url_detail, {"idea_text": "Partial update my first idea test!"})
        idea = Idea.objects.get(id=self.idea.id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)        
        self.assertEqual(response.data.get("idea_text"), idea.idea_text)

    def test_idea_object_delete_authorization(self):
        """Test DELETE HTTP method with other user token."""

        self.api_authentication(self.other_user_token.key)
        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_idea_object_delete(self):
        """Test DELETE HTTP method with the logged in user."""

        response = self.client.delete(self.url_detail)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        