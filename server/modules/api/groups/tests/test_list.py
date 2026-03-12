from django.contrib.auth.models import Group
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class ListGroupsTests(GroupEndpointTestBase):

    def test_list_empty(self):
        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'], [])

    def test_list_returns_user_groups(self):
        g1 = Group.objects.create(name='alpha')
        g2 = Group.objects.create(name='beta')
        self.user.groups.add(g1, g2)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        names = [g['name'] for g in response.data['groups']]
        self.assertEqual(names, ['alpha', 'beta'])

    def test_list_excludes_other_user_groups(self):
        g = Group.objects.create(name='secret')
        self.other_user.groups.add(g)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'], [])

    def test_list_includes_member_count(self):
        g = Group.objects.create(name='team')
        self.user.groups.add(g)
        self.other_user.groups.add(g)

        response = self.authenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['groups'][0]['member_count'], 2)

    def test_list_unauthenticated(self):
        response = self.unauthenticated_client.get('/api/groups/')
        self.assertEqual(response.status_code, 401)
