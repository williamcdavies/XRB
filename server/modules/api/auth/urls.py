from .           import views
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path('start/', views.start, name='start'),
]