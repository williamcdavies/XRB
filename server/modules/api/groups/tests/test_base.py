import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient

from modules.api.groups.models import GroupMembership

User = get_user_model()

class GroupEndpointTestBase(APITestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.patcher = patch('modules.api.groups.views.BASE_DATA_DIR', self.tmp)
        self.patcher.start()

        (self.tmp / 'groups').mkdir()

        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com')

        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)

        self.other_client = APIClient()
        self.other_client.force_authenticate(user=self.other_user)

        self.unauthenticated_client = APIClient()

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _create_group_with_admin(self, name, admin_user):
        """Helper to create a group and add a user as admin."""
        group = Group.objects.create(name=name)
        admin_user.groups.add(group)
        GroupMembership.objects.create(user=admin_user, group=group, role=GroupMembership.ROLE_ADMIN)
        return group

    def _add_member(self, group, user, role=GroupMembership.ROLE_USER):
        """Helper to add a user to a group with a role."""
        user.groups.add(group)
        return GroupMembership.objects.create(user=user, group=group, role=role)
