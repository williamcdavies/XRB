from .           import views
from django.urls import path

app_name = 'account'
urlpatterns = [
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('update_name/', views.update_name, name='update_name'),
    path('update_email/', views.update_email, name='update_email'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('update_language/', views.update_language, name='update_language'),
    path('update_type/', views.update_type, name='update_type'),
    path('delete_account/', views.delete_account, name='delete_account'),
]