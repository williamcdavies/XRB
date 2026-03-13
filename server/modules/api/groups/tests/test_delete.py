from django.contrib.auth.models import Group
from modules.api.groups.models import GroupMembership
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class DeleteGroupTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = self._create_group_with_admin('test-group', self.user)

    def test_admin_delete_group(self):
        response = self.authenticated_client.delete(f'/api/groups/{self.group.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

    def test_user_cannot_delete_group(self):
        self._add_member(self.group, self.other_user, role=GroupMembership.ROLE_USER)
        response = self.other_client.delete(f'/api/groups/{self.group.id}/delete/')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Group.objects.filter(id=self.group.id).exists())

    def test_delete_nonexistent_group(self):
        response = self.authenticated_client.delete('/api/groups/99999/delete/')
        self.assertEqual(response.status_code, 404)

    def test_delete_non_member_denied(self):
        response = self.other_client.delete(f'/api/groups/{self.group.id}/delete/')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Group.objects.filter(id=self.group.id).exists())

    def test_delete_unauthenticated(self):
        response = self.unauthenticated_client.delete(f'/api/groups/{self.group.id}/delete/')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Group.objects.filter(id=self.group.id).exists())
