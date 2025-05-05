from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('new/', views.new_thread, name='new_thread'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)