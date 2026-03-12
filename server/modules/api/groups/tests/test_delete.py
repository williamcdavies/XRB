from django.contrib.auth.models import Group
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class DeleteGroupTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = Group.objects.create(name='test-group')
        self.user.groups.add(self.group)

    def test_delete_group(self):
        response = self.authenticated_client.delete(f'/api/groups/{self.group.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

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
