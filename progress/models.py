from django.db import models
from django.contrib.auth.models import User
from plans.models import Plan, Exercise


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.date}'


class ExerciseLog(models.Model):
    workout_log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name='exercise_logs')
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, blank=True)
    exercise_name = models.CharField(max_length=200)
    sets_done = models.PositiveIntegerField(default=0)
    reps_done = models.PositiveIntegerField(default=0)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.exercise_name} - {self.workout_log.date}'


class BodyWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='body_weights')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.weight_kg}kg - {self.date}'
