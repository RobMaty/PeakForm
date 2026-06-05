from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile
from .forms import RegisterForm


class ProfileSignalTests(TestCase):
    def test_profile_created_with_user(self):
        user = User.objects.create_user(username='tester', password='pass12345')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str(self):
        user = User.objects.create_user(username='tester', password='pass12345')
        self.assertEqual(str(user.profile), 'tester Profile')


class RegisterFormTests(TestCase):
    def test_valid_data_is_accepted(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords_rejected(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'Different123',
        })
        self.assertFalse(form.is_valid())


class RegisterViewTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')

    def test_valid_login(self):
        response = self.client.post(reverse('login'), data={'username': 'tester', 'password': 'pass12345'})
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), data={'username': 'tester', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')

    def test_profile_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_update_saves_changes(self):
        response = self.client.post(reverse('profile'), data={
            'bio': 'Aiming for the top',
            'goal': 'build_muscle',
            'weight': '82.00',
            'height': '180.00',
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.goal, 'build_muscle')
        self.assertEqual(self.user.profile.bio, 'Aiming for the top')
