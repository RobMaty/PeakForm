from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Plan, UserPlan


def home(request):
    plans = Plan.objects.all().order_by('-created_at')
    return render(request, 'plans/home.html', {'plans': plans})


def plan_detail(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = UserPlan.objects.filter(user=request.user, plan=plan).exists()
    return render(request, 'plans/detail.html', {'plan': plan, 'is_enrolled': is_enrolled})


@login_required
def enroll_plan(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        plan = get_object_or_404(Plan, pk=pk)
        user_plan, created = UserPlan.objects.get_or_create(user=request.user, plan=plan)
        if not created:
            user_plan.delete()
            return JsonResponse({'enrolled': False, 'message': 'Unenrolled from plan.'})
        return JsonResponse({'enrolled': True, 'message': f'Enrolled in {plan.title}!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def my_plans(request):
    user_plans = UserPlan.objects.filter(user=request.user, is_active=True).select_related('plan')
    return render(request, 'plans/my_plans.html', {'user_plans': user_plans})
