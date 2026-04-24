from .           import views
from django.urls import path

app_name = 'account'
urlpatterns = [
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('update_name/', views.update_name, name='update_name'),
    path('send_email_change/', views.send_email_change, name='send-email-change'),
    path('verify_email_change/', views.verify_email_change, name='verify-email-change'),
    path('update_email/', views.update_email, name='update_email'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('update_language/', views.update_language, name='update_language'),
    path('update_type/', views.update_type, name='update_type'),
    path('logout/', views.logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('rsync_keys/', views.list_rsync_keys, name='list_rsync_keys'),
    path('rsync_keys/create/', views.create_rsync_key, name='create_rsync_key'),
    path('rsync_keys/<int:key_id>/', views.delete_rsync_key, name='delete_rsync_key'),
]