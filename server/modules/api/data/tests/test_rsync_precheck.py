from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from modules.api.data.rsync_precheck import evaluate, normalize, split_paths
from modules.api.groups.models import FileAccessControl, GroupMembership

User = get_user_model()


def server_argv(paths, sender=False):
    args = ['rsync', '--server']
    if sender:
        args.append('--sender')
    args.extend(['-vlogDtpre.iLsfxC', '.'])
    args.extend(paths)
    return args


class NormalizeTests(TestCase):
    def test_basic(self):
        self.assertEqual(normalize('users/me/foo.csv'), 'users/me/foo.csv')

    def test_strips_leading_slash(self):
        self.assertEqual(normalize('/public/x'), 'public/x')

    def test_resolves_dot(self):
        self.assertEqual(normalize('public/./x'), 'public/x')

    def test_collapses_inner_dotdot(self):
        self.assertEqual(normalize('users/me/../me/foo'), 'users/me/foo')

    def test_rejects_escape(self):
        self.assertIsNone(normalize('../etc/passwd'))
        self.assertIsNone(normalize('users/../../etc'))


class SplitPathsTests(TestCase):
    def test_sender_detected(self):
        is_sender, paths = split_paths(server_argv(['public/x'], sender=True))
        self.assertTrue(is_sender)
        self.assertEqual(paths, ['public/x'])

    def test_receiver(self):
        is_sender, paths = split_paths(server_argv(['users/me/'], sender=False))
        self.assertFalse(is_sender)
        self.assertEqual(paths, ['users/me/'])

    def test_no_separator(self):
        _, paths = split_paths(['rsync', '--server', '--sender', '-x'])
        self.assertIsNone(paths)


class EvaluateTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice@example.com', email='alice@example.com')
        self.bob = User.objects.create_user(username='bob@example.com', email='bob@example.com')
        self.group = Group.objects.create(name='astro-lab')
        self.alice.groups.add(self.group)
        GroupMembership.objects.create(user=self.alice, group=self.group, role=GroupMembership.ROLE_USER)

    def test_pull_public_allowed(self):
        ok, _ = evaluate(self.alice, server_argv(['public/sample.csv'], sender=True))
        self.assertTrue(ok)

    def test_push_to_own_user_dir_allowed(self):
        ok, _ = evaluate(self.alice, server_argv(['users/alice@example.com/foo.csv'], sender=False))
        self.assertTrue(ok)

    def test_push_to_other_user_denied(self):
        ok, reason = evaluate(self.alice, server_argv(['users/bob@example.com/foo.csv'], sender=False))
        self.assertFalse(ok)
        self.assertIn('not_owner', reason)

    def test_pull_other_user_denied(self):
        ok, reason = evaluate(self.alice, server_argv(['users/bob@example.com/foo.csv'], sender=True))
        self.assertFalse(ok)
        self.assertIn('not_owner', reason)

    def test_pull_unaffiliated_group_denied(self):
        ok, reason = evaluate(self.alice, server_argv(['groups/secret/x.csv'], sender=True))
        self.assertFalse(ok)
        self.assertIn('not_group_member', reason)

    def test_pull_group_member_allowed(self):
        ok, _ = evaluate(self.alice, server_argv(['groups/astro-lab/notes.csv'], sender=True))
        self.assertTrue(ok)

    def test_path_escape_denied(self):
        ok, reason = evaluate(self.alice, server_argv(['../etc/passwd'], sender=True))
        self.assertFalse(ok)
        self.assertIn('escapes', reason)

    def test_no_paths_denied(self):
        ok, _ = evaluate(self.alice, ['rsync', '--server', '--sender', '-x'])
        self.assertFalse(ok)

    def test_descendant_deny_blocks_directory_pull(self):
        FileAccessControl.objects.create(group=self.group, path='restricted/x.csv')
        ok, reason = evaluate(self.alice, server_argv(['groups/astro-lab/'], sender=True))
        self.assertFalse(ok)
        self.assertIn('narrow your request', reason)

    def test_descendant_deny_does_not_block_sibling_pull(self):
        FileAccessControl.objects.create(group=self.group, path='restricted/x.csv')
        ok, _ = evaluate(self.alice, server_argv(['groups/astro-lab/open/y.csv'], sender=True))
        self.assertTrue(ok)

    def test_descendant_deny_skipped_for_admin(self):
        admin_user = User.objects.create_user(username='admin@example.com', email='admin@example.com')
        admin_user.groups.add(self.group)
        GroupMembership.objects.create(user=admin_user, group=self.group, role=GroupMembership.ROLE_ADMIN)
        FileAccessControl.objects.create(group=self.group, path='restricted/x.csv')
        ok, _ = evaluate(admin_user, server_argv(['groups/astro-lab/'], sender=True))
        self.assertTrue(ok)

    def test_descendant_deny_skipped_when_user_explicitly_allowed(self):
        fac = FileAccessControl.objects.create(group=self.group, path='restricted/x.csv')
        fac.allowed_users.add(self.alice)
        ok, _ = evaluate(self.alice, server_argv(['groups/astro-lab/'], sender=True))
        self.assertTrue(ok)
