from django.db import models
from django.contrib.auth.models import User, Group
import os

def user_directory_path(instance, filename):
    """Files will be uploaded to /media/users/{username}/{filename}"""
    return f'users/{instance.user.username}/{filename}'

def group_directory_path(instance, filename):
    """Files will be uploaded to /media/groups/{groupname}/{filename}"""
    return f'groups/{instance.group.name}/{filename}'

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_directory_path)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()  # in bytes
    
    class Meta:
        db_table = 'user_files'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.username}/{self.filename}"

class GroupFile(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=group_directory_path)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()
    
    class Meta:
        db_table = 'group_files'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.group.name}/{self.filename}"

class SharedFile(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='shared/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()
    
    class Meta:
        db_table = 'shared_files'
        ordering = ['-uploaded_at']