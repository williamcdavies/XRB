from . import views
from django.urls import path

app_name = 'data'

urlpatterns = [
    path('file/', views.get_file_data, name='get_file_data'),
]
