from django.contrib import admin
from .models import WorkoutLog, ExerciseLog, BodyWeight

class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 0

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'completed', 'created_at']
    list_filter = ['completed']
    inlines = [ExerciseLogInline]

@admin.register(BodyWeight)
class BodyWeightAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight_kg', 'date']
