from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import WorkoutLog, ExerciseLog, BodyWeight
import json


@login_required
def dashboard(request):
    logs = WorkoutLog.objects.filter(user=request.user).select_related('plan')[:10]
    weights = BodyWeight.objects.filter(user=request.user)[:10]
    completed_count = WorkoutLog.objects.filter(user=request.user, completed=True).count()
    return render(request, 'progress/dashboard.html', {'logs': logs, 'weights': weights, 'completed_count': completed_count})


@login_required
def log_workout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        log = WorkoutLog.objects.create(
            user=request.user,
            date=data.get('date', timezone.now().date()),
            notes=data.get('notes', ''),
            completed=data.get('completed', False),
        )
        return JsonResponse({'success': True, 'log_id': log.id})
    logs = WorkoutLog.objects.filter(user=request.user)[:20]
    return render(request, 'progress/log_workout.html', {'logs': logs})


@login_required
def log_weight(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        entry = BodyWeight.objects.create(
            user=request.user,
            weight_kg=data['weight_kg'],
            date=data.get('date', str(timezone.now().date())),
        )
        return JsonResponse({'success': True, 'id': entry.id, 'weight': str(entry.weight_kg), 'date': str(entry.date)})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def weight_history(request):
    weights = BodyWeight.objects.filter(user=request.user).order_by('date').values('date', 'weight_kg')
    data = [{'date': str(w['date']), 'weight': float(w['weight_kg'])} for w in weights]
    return JsonResponse({'data': data})
