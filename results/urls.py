from django.urls import path
from .views import (assessment_list, assessment_detail, 
                   create_assessment, create_result, upload_results)

urlpatterns = [
    path('', assessment_list, name='assessment_list'),
    path('assessment/<int:pk>/', assessment_detail, name='assessment_detail'),
    path('assessment/new/', create_assessment, name='create_assessment'),
    path('assessment/<int:assessment_id>/result/new/', create_result, name='create_result'),
    path('upload/', upload_results, name='upload_results'),
]