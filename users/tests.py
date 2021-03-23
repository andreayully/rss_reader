from django.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model


class SignUpTest(TestCase):
    def setUp(self):
        self.dummy_user = mommy.make(User)
        user = self.dummy_user
        user.username = 'test'
        user.password = 'test123*'
        user.save()

    def test_create_user(self):
        self.assertTrue(isinstance(self.dummy_user, User))

    def test_create_user_view(self):
        response = self.client.get(reverse('rss:create-user'),
                                   {'first_name': 'Ana',
                                    'last_name': 'Gonzales',
                                    'email': 'ana@gmail.com',
                                    'password1': 'test123*',
                                    'password2': 'test123*'
                                    })
        self.assertEqual(response.status_code, 200)


class SignInTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test123*', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct_user(self):
        user = authenticate(username='test', password='test123*')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_user(self):
        dummy_user = mommy.make(User)
        user = authenticate(username=dummy_user.username, password=dummy_user.password)
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_signin_view(self):
        response = self.client.get(reverse('rss:login'), {'username': 'test', 'password': 'test123*'})
        self.assertEqual(response.status_code, 200)
