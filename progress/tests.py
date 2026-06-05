import json
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import WorkoutLog, BodyWeight, validate_not_future


class ValidateNotFutureTests(TestCase):
    def test_today_is_allowed(self):
        self.assertIsNone(validate_not_future(timezone.now().date()))

    def test_past_is_allowed(self):
        self.assertIsNone(validate_not_future(timezone.now().date() - timedelta(days=30)))

    def test_future_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_future(timezone.now().date() + timedelta(days=1))


class WorkoutLogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')

    def test_valid_workout_passes_full_clean(self):
        log = WorkoutLog(user=self.user, date=timezone.now().date(), notes='Leg day')
        log.full_clean(exclude=['plan'])
        log.save()
        self.assertEqual(WorkoutLog.objects.count(), 1)

    def test_future_workout_fails_full_clean(self):
        log = WorkoutLog(user=self.user, date=timezone.now().date() + timedelta(days=2))
        with self.assertRaises(ValidationError):
            log.full_clean(exclude=['plan'])


class BodyWeightModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')

    def test_valid_weight_passes_full_clean(self):
        entry = BodyWeight(user=self.user, weight_kg='80.50', date=timezone.now().date())
        entry.full_clean()
        entry.save()
        self.assertEqual(BodyWeight.objects.count(), 1)

    def test_future_weight_fails_full_clean(self):
        entry = BodyWeight(user=self.user, weight_kg='80.50', date=timezone.now().date() + timedelta(days=1))
        with self.assertRaises(ValidationError):
            entry.full_clean()


class LogWorkoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')
        self.url = reverse('log_workout')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_valid_workout_is_created(self):
        payload = {'date': str(timezone.now().date()), 'notes': 'Push day', 'completed': True}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(WorkoutLog.objects.filter(user=self.user).count(), 1)

    def test_future_workout_is_rejected(self):
        future = str(timezone.now().date() + timedelta(days=5))
        payload = {'date': future, 'notes': 'Time travel'}
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
        self.assertEqual(WorkoutLog.objects.count(), 0)


class LogWeightViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')
        self.url = reverse('log_weight')

    def test_valid_weight_is_created(self):
        payload = {'weight_kg': 79.4, 'date': str(timezone.now().date())}
        response = self.client.post(
            self.url, data=json.dumps(payload),
            content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(BodyWeight.objects.filter(user=self.user).count(), 1)

    def test_future_weight_is_rejected(self):
        payload = {'weight_kg': 79.4, 'date': str(timezone.now().date() + timedelta(days=3))}
        response = self.client.post(
            self.url, data=json.dumps(payload),
            content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BodyWeight.objects.count(), 0)


class WeightHistoryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')

    def test_history_returns_logged_weights(self):
        BodyWeight.objects.create(user=self.user, weight_kg='81.00', date=timezone.now().date())
        response = self.client.get(reverse('weight_history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 1)
