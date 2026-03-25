from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='progress_dashboard'),
    path('log/', views.log_workout, name='log_workout'),
    path('weight/', views.log_weight, name='log_weight'),
    path('weight/history/', views.weight_history, name='weight_history'),
]
