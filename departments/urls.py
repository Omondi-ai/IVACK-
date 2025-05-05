from django.urls import path
from .views import (department_list, department_detail, 
                   create_department, create_course)

urlpatterns = [
    path('', department_list, name='department_list'),
    path('<int:pk>/', department_detail, name='department_detail'),
    path('new/', create_department, name='create_department'),
    path('course/new/', create_course, name='create_course'),
]