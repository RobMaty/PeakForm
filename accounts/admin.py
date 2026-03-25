from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'weight', 'height', 'created_at']
    list_filter = ['goal']
    search_fields = ['user__username', 'user__email']
