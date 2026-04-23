import base64
import struct
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from modules.api.account.models import RsyncPublicKey
from modules.api.account.rsync_authorized_keys import WRAPPER_PATH

User = get_user_model()


def make_ed25519_key(seed: bytes = b'\x01' * 32, comment: str = '') -> str:
    algo = b'ssh-ed25519'
    blob = (
        struct.pack('>I', len(algo)) + algo
        + struct.pack('>I', len(seed)) + seed
    )
    line = 'ssh-ed25519 ' + base64.b64encode(blob).decode()
    if comment:
        line += ' ' + comment
    return line


class RsyncKeyTestBase(APITestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.auth_keys_path = self.tmp / 'authorized_keys'
        self.patcher = patch(
            'modules.api.account.rsync_authorized_keys._authorized_keys_path',
            return_value=self.auth_keys_path,
        )
        self.patcher.start()

        self.user = User.objects.create_user(username='alice@example.com', email='alice@example.com')
        self.other = User.objects.create_user(username='bob@example.com', email='bob@example.com')

        self.client_alice = APIClient()
        self.client_alice.force_authenticate(user=self.user)
        self.client_bob = APIClient()
        self.client_bob.force_authenticate(user=self.other)
        self.unauth = APIClient()

        self.key_alice_1 = make_ed25519_key(seed=b'A' * 32, comment='alice@laptop')
        self.key_alice_2 = make_ed25519_key(seed=b'B' * 32, comment='alice@desktop')
        self.key_bob_1 = make_ed25519_key(seed=b'C' * 32, comment='bob@laptop')

    def tearDown(self):
        self.patcher.stop()


class RsyncKeyAPITests(RsyncKeyTestBase):
    def test_list_empty(self):
        r = self.client_alice.get('/api/account/rsync_keys/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, [])

    def test_create_returns_fingerprint(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['name'], 'laptop')
        self.assertEqual(r.data['key_type'], 'ssh-ed25519')
        self.assertTrue(r.data['fingerprint'].startswith('SHA256:'))
        self.assertNotIn('public_key', r.data)

    def test_create_requires_name_and_key(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'public_key': self.key_alice_1},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop'},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_invalid_key(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': 'not-a-key'},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_unsupported_type(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': 'ssh-dss AAAA'},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_multiline(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1 + '\nevil-second-line'},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_duplicate_name(self):
        self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_2},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_duplicate_fingerprint(self):
        self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'other', 'public_key': self.key_alice_1},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_same_key_across_users(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        self.assertEqual(r.status_code, 201)
        # Bob cannot register the same public key — fingerprints are global.
        r = self.client_bob.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_delete_owner_only(self):
        r = self.client_alice.post(
            '/api/account/rsync_keys/create/',
            {'name': 'laptop', 'public_key': self.key_alice_1},
            format='json',
        )
        key_id = r.data['id']

        r = self.client_bob.delete(f'/api/account/rsync_keys/{key_id}/')
        self.assertEqual(r.status_code, 404)

        r = self.client_alice.delete(f'/api/account/rsync_keys/{key_id}/')
        self.assertEqual(r.status_code, 204)
        self.assertFalse(RsyncPublicKey.objects.filter(pk=key_id).exists())

    def test_unauthenticated(self):
        self.assertEqual(self.unauth.get('/api/account/rsync_keys/').status_code, 401)
        self.assertEqual(
            self.unauth.post('/api/account/rsync_keys/create/', {'name': 'x'}, format='json').status_code,
            401,
        )


class AuthorizedKeysRegenerationTests(RsyncKeyTestBase):
    def _post(self, client, name, key):
        return client.post(
            '/api/account/rsync_keys/create/',
            {'name': name, 'public_key': key},
            format='json',
        )

    def test_file_written_on_create(self):
        self._post(self.client_alice, 'laptop', self.key_alice_1)
        self.assertTrue(self.auth_keys_path.exists())
        body = self.auth_keys_path.read_text()
        self.assertIn(f'command="{WRAPPER_PATH} alice@example.com"', body)
        self.assertIn(self.key_alice_1, body)
        self.assertEqual(self.auth_keys_path.stat().st_mode & 0o777, 0o600)

    def test_file_updated_on_delete(self):
        r = self._post(self.client_alice, 'laptop', self.key_alice_1)
        self.client_alice.delete(f'/api/account/rsync_keys/{r.data["id"]}/')
        self.assertEqual(self.auth_keys_path.read_text(), '')

    def test_multiple_users_in_same_file(self):
        self._post(self.client_alice, 'laptop', self.key_alice_1)
        self._post(self.client_bob, 'laptop', self.key_bob_1)
        body = self.auth_keys_path.read_text().strip().splitlines()
        self.assertEqual(len(body), 2)
        self.assertTrue(any(f'{WRAPPER_PATH} alice@example.com' in line for line in body))
        self.assertTrue(any(f'{WRAPPER_PATH} bob@example.com' in line for line in body))

    def test_line_pins_forced_command_options(self):
        self._post(self.client_alice, 'laptop', self.key_alice_1)
        line = self.auth_keys_path.read_text().strip()
        for opt in ('no-pty', 'no-port-forwarding', 'no-agent-forwarding', 'no-X11-forwarding'):
            self.assertIn(opt, line)
