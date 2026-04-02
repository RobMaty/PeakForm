from django.db import migrations


MOCK_PLANS = [
    {
        'title': 'Foundation Alpha',
        'description': 'Build an unbreakable strength foundation with compound lifts and progressive overload. Designed for those ready to commit to structured barbell training across 8 disciplined weeks.',
        'level': 'intermediate',
        'duration_weeks': 8,
        'price': '29.99',
        'is_free': False,
        'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
    },
    {
        'title': 'HyperTrophy Max',
        'description': 'Maximum muscle stimulation through high-volume training, progressive tension, and strategic rest. Dedicated to advanced athletes pursuing serious hypertrophy in 12 intensive weeks.',
        'level': 'advanced',
        'duration_weeks': 12,
        'price': '39.99',
        'is_free': False,
        'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
    },
    {
        'title': 'Kinetic Sprinter',
        'description': 'Custom speed, power and conditioning protocol for competitive athletes. Combines sprint mechanics, plyometrics and strength conditioning to unlock peak athletic performance in 10 weeks.',
        'level': 'advanced',
        'duration_weeks': 10,
        'price': '49.99',
        'is_free': False,
        'image_url': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=600&q=80',
    },
]

MOCK_EXERCISES = {
    'Foundation Alpha': [
        {'name': 'Barbell Back Squat', 'sets': 4, 'reps': 5, 'rest_seconds': 180, 'day_of_week': 1},
        {'name': 'Conventional Deadlift', 'sets': 3, 'reps': 5, 'rest_seconds': 180, 'day_of_week': 1},
        {'name': 'Bench Press', 'sets': 4, 'reps': 6, 'rest_seconds': 120, 'day_of_week': 2},
        {'name': 'Overhead Press', 'sets': 3, 'reps': 8, 'rest_seconds': 120, 'day_of_week': 2},
        {'name': 'Barbell Row', 'sets': 4, 'reps': 6, 'rest_seconds': 120, 'day_of_week': 3},
        {'name': 'Romanian Deadlift', 'sets': 3, 'reps': 8, 'rest_seconds': 120, 'day_of_week': 3},
    ],
    'HyperTrophy Max': [
        {'name': 'Incline Dumbbell Press', 'sets': 4, 'reps': 10, 'rest_seconds': 90, 'day_of_week': 1},
        {'name': 'Cable Flyes', 'sets': 3, 'reps': 15, 'rest_seconds': 60, 'day_of_week': 1},
        {'name': 'Pull-Ups', 'sets': 4, 'reps': 10, 'rest_seconds': 90, 'day_of_week': 2},
        {'name': 'Seated Cable Row', 'sets': 4, 'reps': 12, 'rest_seconds': 75, 'day_of_week': 2},
        {'name': 'Leg Press', 'sets': 5, 'reps': 12, 'rest_seconds': 90, 'day_of_week': 3},
        {'name': 'Leg Curl', 'sets': 4, 'reps': 12, 'rest_seconds': 75, 'day_of_week': 3},
        {'name': 'Lateral Raises', 'sets': 4, 'reps': 15, 'rest_seconds': 60, 'day_of_week': 4},
        {'name': 'Tricep Pushdown', 'sets': 3, 'reps': 15, 'rest_seconds': 60, 'day_of_week': 4},
    ],
    'Kinetic Sprinter': [
        {'name': '30m Sprint Intervals', 'sets': 8, 'reps': 1, 'rest_seconds': 120, 'day_of_week': 1},
        {'name': 'Box Jumps', 'sets': 4, 'reps': 6, 'rest_seconds': 90, 'day_of_week': 1},
        {'name': 'Power Clean', 'sets': 5, 'reps': 3, 'rest_seconds': 150, 'day_of_week': 2},
        {'name': 'Broad Jump', 'sets': 4, 'reps': 5, 'rest_seconds': 90, 'day_of_week': 2},
        {'name': 'Single-Leg RDL', 'sets': 3, 'reps': 10, 'rest_seconds': 75, 'day_of_week': 3},
        {'name': 'Hill Sprints', 'sets': 6, 'reps': 1, 'rest_seconds': 120, 'day_of_week': 4},
    ],
}


def create_mock_plans(apps, schema_editor):
    Plan = apps.get_model('plans', 'Plan')
    Exercise = apps.get_model('plans', 'Exercise')
    for data in MOCK_PLANS:
        if Plan.objects.filter(title=data['title']).exists():
            continue
        plan = Plan.objects.create(**data)
        for ex in MOCK_EXERCISES.get(data['title'], []):
            Exercise.objects.create(plan=plan, **ex)


def delete_mock_plans(apps, schema_editor):
    Plan = apps.get_model('plans', 'Plan')
    Plan.objects.filter(title__in=[p['title'] for p in MOCK_PLANS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_plan_image_url'),
    ]

    operations = [
        migrations.RunPython(create_mock_plans, delete_mock_plans),
    ]
