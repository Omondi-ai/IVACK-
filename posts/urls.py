from django.urls import path
from .views import post_list, post_detail, create_post

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('new/', create_post, name='create_post'),
]