from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Plan, UserPlan
from .forms import PlanForm


def landing(request):
    plans = Plan.objects.all().order_by('-created_at')[:6]
    return render(request, 'landing.html', {'plans': plans})


@login_required
def home(request):
    plans = Plan.objects.all().order_by('-created_at')
    return render(request, 'plans/home.html', {'plans': plans})


@login_required
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


@login_required
def create_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            messages.success(request, f'Plan "{plan.title}" created successfully!')
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = PlanForm()
    return render(request, 'plans/plan_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f'Plan "{plan.title}" updated successfully!')
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = PlanForm(instance=plan)
    return render(request, 'plans/plan_form.html', {'form': form, 'action': 'Edit', 'plan': plan})
