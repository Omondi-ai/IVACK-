from django import forms
from .models import Department, Course

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'logo', 'banner_image', 'theme_color']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['department', 'code', 'name', 'description', 'syllabus']