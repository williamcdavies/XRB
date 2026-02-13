from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'data'

router = DefaultRouter()

urlpatterns = [
    path('file/', views.get_file, name='get_file_data'),
    path('download/', views.download_file, name='download_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('browse/', views.browse_files, name='browse_files'),
]
