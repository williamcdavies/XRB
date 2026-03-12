from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from modules.api.groups.tests.test_base import GroupEndpointTestBase

User = get_user_model()


class AddMemberTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = Group.objects.create(name='test-group')
        self.user.groups.add(self.group)

    def test_add_member(self):
        response = self.authenticated_client.post(
            f'/api/groups/{self.group.id}/members/',
            {'email': 'other@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], 'other@example.com')
        self.assertTrue(self.other_user.groups.filter(id=self.group.id).exists())

    def test_add_member_already_in_group(self):
        self.other_user.groups.add(self.group)
        response = self.authenticated_client.post(
            f'/api/groups/{self.group.id}/members/',
            {'email': 'other@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 409)

    def test_add_member_nonexistent_email(self):
        response = self.authenticated_client.post(
            f'/api/groups/{self.group.id}/members/',
            {'email': 'nobody@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)

    def test_add_member_missing_email(self):
        response = self.authenticated_client.post(
            f'/api/groups/{self.group.id}/members/',
            {},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_add_member_non_member_denied(self):
        response = self.other_client.post(
            f'/api/groups/{self.group.id}/members/',
            {'email': 'other@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)

    def test_add_member_unauthenticated(self):
        response = self.unauthenticated_client.post(
            f'/api/groups/{self.group.id}/members/',
            {'email': 'other@example.com'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)


class RemoveMemberTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = Group.objects.create(name='test-group')
        self.user.groups.add(self.group)
        self.other_user.groups.add(self.group)

    def test_remove_member(self):
        response = self.authenticated_client.delete(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.other_user.groups.filter(id=self.group.id).exists())

    def test_remove_self(self):
        response = self.authenticated_client.delete(
            f'/api/groups/{self.group.id}/members/{self.user.id}/'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.user.groups.filter(id=self.group.id).exists())

    def test_remove_nonexistent_member(self):
        response = self.authenticated_client.delete(
            f'/api/groups/{self.group.id}/members/99999/'
        )
        self.assertEqual(response.status_code, 404)

    def test_remove_member_non_member_denied(self):
        third_user = User.objects.create_user(username='third', email='third@example.com')
        third_client = self.client_class()
        third_client.force_authenticate(user=third_user)

        response = third_client.delete(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/'
        )
        self.assertEqual(response.status_code, 404)

    def test_remove_member_unauthenticated(self):
        response = self.unauthenticated_client.delete(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/'
        )
        self.assertEqual(response.status_code, 401)
