from .           import views
from django.urls import path


app_name    = 'account'
urlpatterns = [
    path('get_user_info/', views.get_user_info, name='get_user_info')
]