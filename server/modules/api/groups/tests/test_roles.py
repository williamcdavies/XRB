from django.contrib.auth import get_user_model
from modules.api.groups.models import GroupMembership
from modules.api.groups.tests.test_base import GroupEndpointTestBase

User = get_user_model()


class UpdateRoleTests(GroupEndpointTestBase):

    def setUp(self):
        super().setUp()
        self.group = self._create_group_with_admin('test-group', self.user)
        self._add_member(self.group, self.other_user, role=GroupMembership.ROLE_USER)

    def test_promote_to_admin(self):
        response = self.authenticated_client.patch(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/role/',
            {'role': 'admin'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'admin')
        self.other_user.refresh_from_db()
        membership = GroupMembership.objects.get(user=self.other_user, group=self.group)
        self.assertEqual(membership.role, GroupMembership.ROLE_ADMIN)

    def test_demote_to_user(self):
        # First promote other_user to admin
        target = GroupMembership.objects.get(user=self.other_user, group=self.group)
        target.role = GroupMembership.ROLE_ADMIN
        target.save()

        response = self.authenticated_client.patch(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/role/',
            {'role': 'user'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'user')
        membership = GroupMembership.objects.get(user=self.other_user, group=self.group)
        self.assertEqual(membership.role, GroupMembership.ROLE_USER)

    def test_non_admin_cannot_change_role(self):
        response = self.other_client.patch(
            f'/api/groups/{self.group.id}/members/{self.user.id}/role/',
            {'role': 'user'},
            format='json',
        )
        self.assertEqual(response.status_code, 403)

    def test_cannot_change_own_role(self):
        response = self.authenticated_client.patch(
            f'/api/groups/{self.group.id}/members/{self.user.id}/role/',
            {'role': 'user'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_role(self):
        response = self.authenticated_client.patch(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/role/',
            {'role': 'superadmin'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_member(self):
        response = self.authenticated_client.patch(
            f'/api/groups/{self.group.id}/members/99999/role/',
            {'role': 'admin'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)

    def test_non_member_denied(self):
        third_user = User.objects.create_user(username='third', email='third@example.com')
        third_client = self.client_class()
        third_client.force_authenticate(user=third_user)

        response = third_client.patch(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/role/',
            {'role': 'admin'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated(self):
        response = self.unauthenticated_client.patch(
            f'/api/groups/{self.group.id}/members/{self.other_user.id}/role/',
            {'role': 'admin'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)
