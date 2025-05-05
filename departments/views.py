from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Course
from .forms import DepartmentForm, CourseForm
from posts.models import Post

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    courses = Course.objects.filter(department=department)
    posts = Post.objects.filter(department=department)
    
    context = {
        'department': department,
        'courses': courses,
        'posts': posts,
    }
    return render(request, 'departments/department_detail.html', context)

@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = CourseForm()
    return render(request, 'departments/course_form.html', {'form': form})

def departments_processor(request):
    departments = Department.objects.all()
    return {'all_departments': departments}