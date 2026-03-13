from modules.api.groups.tests.test_base import GroupEndpointTestBase


class ListGroupsTests(GroupEndpointTestBase):

    def test_list_empty(self):
        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'], [])

    def test_list_returns_user_groups(self):
        self._create_group_with_admin('alpha', self.user)
        self._create_group_with_admin('beta', self.user)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        names = [g['name'] for g in response.data['groups']]
        self.assertEqual(names, ['alpha', 'beta'])

    def test_list_excludes_other_user_groups(self):
        self._create_group_with_admin('secret', self.other_user)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'], [])

    def test_list_includes_member_count(self):
        group = self._create_group_with_admin('team', self.user)
        self._add_member(group, self.other_user)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'][0]['member_count'], 2)

    def test_list_unauthenticated(self):
        response = self.unauthenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 401)
