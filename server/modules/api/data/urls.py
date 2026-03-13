from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'data'

router = DefaultRouter()

urlpatterns = [
    path('download/', views.download_file, name='download_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('mkdir/', views.create_directory, name='create_directory'),
    path('delete/', views.delete_file, name='delete_file'),
    path('browse/', views.browse_files, name='browse_files'),
    path('preview/table/', views.preview_table, name='preview_table'),
]
