from django.conf import settings
from django.contrib.auth.models import Group as AuthGroup
from django.db import models


class GroupMembership(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships',
    )
    group = models.ForeignKey(
        AuthGroup,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f'{self.user} - {self.group} ({self.role})'


class FileAccessControl(models.Model):
    """
    per file/directory access restriction for individual users in a group
    """

    group = models.ForeignKey(
        AuthGroup,
        on_delete=models.CASCADE,
        related_name='file_access_controls',
    )
    path = models.CharField(
        max_length=1024,
        help_text='Relative path within the group directory, e.g. "reports/q1.csv" or "secret-data".',
    )
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='file_access_grants',
        blank=True,
    )

    class Meta:
        unique_together = ('group', 'path')

    def __str__(self):
        return f'{self.group.name}: {self.path}'
