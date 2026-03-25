from django.contrib import admin
from .models import Plan, Exercise, UserPlan

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration_weeks', 'price', 'is_free', 'created_at']
    list_filter = ['level', 'is_free']
    search_fields = ['title']
    inlines = [ExerciseInline]

@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'enrolled_at', 'is_active']
