from .models import Department

def departments_processor(request):
    return {
        'all_departments': Department.objects.all()
    }