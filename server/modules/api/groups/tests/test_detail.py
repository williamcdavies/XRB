from django.contrib.auth.models import Group
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class GroupDetailTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = Group.objects.create(name='test-group')
        self.user.groups.add(self.group)

    def test_get_detail(self):
        response = self.authenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'test-group')
        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.data['members'][0]['email'], 'test@example.com')

    def test_detail_shows_all_members(self):
        self.other_user.groups.add(self.group)
        response = self.authenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        emails = [m['email'] for m in response.data['members']]
        self.assertIn('test@example.com', emails)
        self.assertIn('other@example.com', emails)

    def test_detail_non_member_denied(self):
        response = self.other_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 404)

    def test_detail_nonexistent_group(self):
        response = self.authenticated_client.get('/api/groups/99999/')
        self.assertEqual(response.status_code, 404)

    def test_detail_unauthenticated(self):
        response = self.unauthenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 401)
