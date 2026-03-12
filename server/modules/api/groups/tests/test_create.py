from django.contrib.auth.models import Group
from modules.api.groups.tests.test_base import GroupEndpointTestBase


class CreateGroupTests(GroupEndpointTestBase):

    def test_create_group(self):
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {'name': 'new-group'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'new-group')
        self.assertEqual(response.data['member_count'], 1)
        self.assertTrue(Group.objects.filter(name='new-group').exists())
        self.assertTrue(self.user.groups.filter(name='new-group').exists())

    def test_create_group_creates_directory(self):
        self.authenticated_client.post(
            '/api/groups/create/',
            {'name': 'dir-test'},
            format='json',
        )
        self.assertTrue((self.tmp / 'groups' / 'dir-test').is_dir())

    def test_create_duplicate_name(self):
        Group.objects.create(name='existing')
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {'name': 'existing'},
            format='json',
        )
        self.assertEqual(response.status_code, 409)

    def test_create_missing_name(self):
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_empty_name(self):
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {'name': '   '},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_name_with_slash(self):
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {'name': 'bad/name'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_name_with_backslash(self):
        response = self.authenticated_client.post(
            '/api/groups/create/',
            {'name': 'bad\\name'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_unauthenticated(self):
        response = self.unauthenticated_client.post(
            '/api/groups/create/',
            {'name': 'nope'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)
