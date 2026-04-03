from . import views
from django.urls import path

app_name = 'groups'

urlpatterns = [
    path('', views.list_groups, name='list_groups'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/members/', views.add_member, name='add_member'),
    path('<int:group_id>/members/<int:user_id>/', views.remove_member, name='remove_member'),
    path('<int:group_id>/members/<int:user_id>/role/', views.update_role, name='update_role'),
    path('<int:group_id>/file-permissions/', views.list_file_permissions, name='list_file_permissions'),
    path('<int:group_id>/file-permissions/set/', views.set_file_permission, name='set_file_permission'),
    path('<int:group_id>/file-permissions/delete/', views.delete_file_permission, name='delete_file_permission'),
    path('<int:group_id>/delete/', views.delete_group, name='delete_group'),
]
