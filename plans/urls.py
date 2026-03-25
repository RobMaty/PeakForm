from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plans/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('plans/<int:pk>/enroll/', views.enroll_plan, name='enroll_plan'),
    path('plans/my/', views.my_plans, name='my_plans'),
]
