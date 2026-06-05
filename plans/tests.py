from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Plan, Exercise, UserPlan


class PlanModelTests(TestCase):
    def test_plan_str(self):
        plan = Plan.objects.create(title='Foundation Alpha', description='Strength base')
        self.assertEqual(str(plan), 'Foundation Alpha')

    def test_exercise_str(self):
        plan = Plan.objects.create(title='Foundation Alpha', description='Strength base')
        exercise = Exercise.objects.create(plan=plan, name='Back Squat')
        self.assertEqual(str(exercise), 'Back Squat (Foundation Alpha)')

    def test_exercises_related_to_plan(self):
        plan = Plan.objects.create(title='Foundation Alpha', description='Strength base')
        Exercise.objects.create(plan=plan, name='Back Squat')
        Exercise.objects.create(plan=plan, name='Deadlift')
        self.assertEqual(plan.exercises.count(), 2)


class PlanViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.plan = Plan.objects.create(title='Foundation Alpha', description='Strength base', is_free=True)

    def test_landing_is_public(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_plan_detail_shows_plan(self):
        self.client.login(username='tester', password='pass12345')
        response = self.client.get(reverse('plan_detail', args=[self.plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Foundation Alpha')


class EnrollPlanViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.plan = Plan.objects.create(title='Foundation Alpha', description='Strength base', is_free=True)
        self.client.login(username='tester', password='pass12345')
        self.url = reverse('enroll_plan', args=[self.plan.pk])

    def test_enroll_creates_user_plan(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['enrolled'])
        self.assertTrue(UserPlan.objects.filter(user=self.user, plan=self.plan).exists())

    def test_second_enroll_toggles_off(self):
        self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(response.json()['enrolled'])
        self.assertFalse(UserPlan.objects.filter(user=self.user, plan=self.plan).exists())

    def test_enroll_rejects_non_ajax(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
