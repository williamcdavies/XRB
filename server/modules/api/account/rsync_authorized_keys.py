import os
import tempfile
from pathlib import Path

from django.conf import settings


FORCED_COMMAND_OPTIONS = (
    'no-pty',
    'no-port-forwarding',
    'no-agent-forwarding',
    'no-X11-forwarding',
    'no-user-rc',
)

WRAPPER_PATH = '/usr/local/bin/xrb-rsync-wrapper'


def _authorized_keys_path() -> Path:
    return Path(getattr(settings, 'RSYNC_AUTHORIZED_KEYS_PATH', '/rsync/authorized_keys'))


def _authorized_keys_line(email: str, public_key: str) -> str:
    # Emails never contain shell metacharacters in normal Django auth, but
    # sshd interprets the command= value as a shell string, so be defensive.
    safe_email = email.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
    options = [f'command="{WRAPPER_PATH} {safe_email}"', *FORCED_COMMAND_OPTIONS]
    return f'{",".join(options)} {public_key.strip()}\n'


def regenerate_authorized_keys() -> None:
    """
    Rewrite the sshd authorized_keys file from the current set of
    RsyncPublicKey rows. Each line pins a forced command that carries the
    Django user's email so the rsync wrapper can enforce per-user access.
    """
    from modules.api.account.models import RsyncPublicKey

    path = _authorized_keys_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = (
        RsyncPublicKey.objects
        .select_related('user')
        .order_by('user__email', 'created_at')
    )
    body = ''.join(
        _authorized_keys_line(k.user.email, k.public_key)
        for k in rows
        if (k.user.email or '').strip()
    )

    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix='.authorized_keys.')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(body)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
