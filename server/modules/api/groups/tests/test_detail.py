from modules.api.groups.models import GroupMembership
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class GroupDetailTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = self._create_group_with_admin('test-group', self.user)

    def test_get_detail(self):
        response = self.authenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'test-group')
        self.assertEqual(response.data['current_user_role'], 'admin')
        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.data['members'][0]['email'], 'test@example.com')
        self.assertEqual(response.data['members'][0]['role'], 'admin')

    def test_detail_shows_all_members_with_roles(self):
        self._add_member(self.group, self.other_user, role=GroupMembership.ROLE_USER)
        response = self.authenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        members_by_email = {m['email']: m for m in response.data['members']}
        self.assertEqual(members_by_email['test@example.com']['role'], 'admin')
        self.assertEqual(members_by_email['other@example.com']['role'], 'user')

    def test_detail_user_role_sees_own_role(self):
        self._add_member(self.group, self.other_user, role=GroupMembership.ROLE_USER)
        response = self.other_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['current_user_role'], 'user')

    def test_detail_non_member_denied(self):
        response = self.other_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 404)

    def test_detail_nonexistent_group(self):
        response = self.authenticated_client.get('/api/groups/99999/')
        self.assertEqual(response.status_code, 404)

    def test_detail_unauthenticated(self):
        response = self.unauthenticated_client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(response.status_code, 401)
