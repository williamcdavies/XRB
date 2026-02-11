from .           import views
from django.urls import path


app_name    = 'auth'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('verify/', views.verify, name='verify'),
    path('refresh/', views.refresh, name='refresh'),
]