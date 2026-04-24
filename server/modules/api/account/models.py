import base64
import hashlib

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    type = models.TextField(null=True)
    preferred_avatar = models.IntegerField(null=True, default=1)
    preferred_language = models.TextField(null=True, default='English')

    class Meta:
        db_table = 'auth_user'


ALLOWED_SSH_KEY_TYPES = frozenset({
    'ssh-rsa',
    'ssh-ed25519',
    'ecdsa-sha2-nistp256',
    'ecdsa-sha2-nistp384',
    'ecdsa-sha2-nistp521',
    'sk-ssh-ed25519@openssh.com',
    'sk-ecdsa-sha2-nistp256@openssh.com',
})


class InvalidPublicKey(ValueError):
    pass


def parse_ssh_public_key(raw):
    """
    Validate a pasted SSH public key and return (key_type, normalized_line, fingerprint).
    ``normalized_line`` is the single-line form that will be written to authorized_keys.
    """
    if raw is None:
        raise InvalidPublicKey('public key is required')
    text = raw.strip()
    if not text:
        raise InvalidPublicKey('public key is required')
    if '\n' in text or '\r' in text:
        raise InvalidPublicKey('public key must be a single line')

    parts = text.split()
    if len(parts) < 2:
        raise InvalidPublicKey('public key must be "<type> <base64>"')

    key_type, key_b64 = parts[0], parts[1]
    if key_type not in ALLOWED_SSH_KEY_TYPES:
        raise InvalidPublicKey(f'unsupported key type: {key_type}')

    try:
        blob = base64.b64decode(key_b64, validate=True)
    except Exception as exc:
        raise InvalidPublicKey('invalid base64 in public key') from exc

    # First field inside the blob must match key_type — cheap sanity check
    # against pasted keys that got mangled.
    if len(blob) < 4:
        raise InvalidPublicKey('public key payload is too short')
    header_len = int.from_bytes(blob[:4], 'big')
    if 4 + header_len > len(blob) or blob[4:4 + header_len].decode('ascii', 'replace') != key_type:
        raise InvalidPublicKey('public key type/payload mismatch')

    digest = hashlib.sha256(blob).digest()
    fingerprint = 'SHA256:' + base64.b64encode(digest).decode('ascii').rstrip('=')
    return key_type, text, fingerprint


class RsyncPublicKey(models.Model):
    """
    Per-user SSH public key authorized to rsync into the XRB data store.
    The ``public_key`` field is the full single-line OpenSSH form
    (``<type> <base64> [comment]``).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsync_public_keys',
    )
    name = models.CharField(max_length=64)
    key_type = models.CharField(max_length=64)
    public_key = models.TextField()
    fingerprint = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'name'),)

    def __str__(self):
        return f'{self.user.email}:{self.name}'

    @classmethod
    def register(cls, user, name, raw_public_key):
        key_type, normalized, fingerprint = parse_ssh_public_key(raw_public_key)
        return cls.objects.create(
            user=user,
            name=name,
            key_type=key_type,
            public_key=normalized,
            fingerprint=fingerprint,
        )
