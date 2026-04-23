"""
Pre-xfer exec hook for the XRB rsync daemon. Invoked by rsyncd before each
transfer; exit 0 to allow, nonzero to abort.

Reads:
  RSYNC_USER_NAME    — authenticated daemon username (a User.email)
  RSYNC_ARG#N        — original argv passed to the rsync server process
  RSYNC_MODULE_PATH  — the on-disk root of the module (we expect /data)

The argv looks like:
    rsync --server [--sender] -<flags> . <path1> <path2> ...
where '.' separates the option block from one or more module-relative paths.
"""

import os
import sys
from pathlib import PurePosixPath


def read_argv_from_env(env=None):
    env = env if env is not None else os.environ
    args = []
    i = 0
    while True:
        v = env.get(f'RSYNC_ARG#{i}')
        if v is None:
            break
        args.append(v)
        i += 1
    return args


def split_paths(argv):
    """Find the '.' separator and return (is_sender, [paths] or None)."""
    is_sender = '--sender' in argv
    try:
        sep = argv.index('.')
    except ValueError:
        return is_sender, None
    return is_sender, argv[sep + 1:]


def normalize(path):
    """Return module-relative path with '..' resolved, or None on escape."""
    if path is None:
        return None
    p = path.lstrip('/')
    parts = []
    for seg in p.split('/'):
        if seg in ('', '.'):
            continue
        if seg == '..':
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(seg)
    return '/'.join(parts)


def has_descendant_deny(user, group_name, sub_path_parts):
    """
    Conservative check: is there any FileAccessControl under sub_path_parts
    that would deny this user? Returns True if a deny exists.
    """
    from django.contrib.auth.models import Group as AuthGroup
    from django.db.models import Q

    from modules.api.groups.models import FileAccessControl, GroupMembership

    try:
        group = AuthGroup.objects.get(name=group_name)
    except AuthGroup.DoesNotExist:
        return False

    is_admin = GroupMembership.objects.filter(
        user=user, group=group, role=GroupMembership.ROLE_ADMIN,
    ).exists()
    if is_admin:
        return False

    prefix = '/'.join(sub_path_parts)
    qs = FileAccessControl.objects.filter(group=group)
    if prefix:
        qs = qs.filter(Q(path=prefix) | Q(path__startswith=prefix + '/'))

    for r in qs.prefetch_related('allowed_users'):
        if not r.allowed_users.filter(id=user.id).exists():
            return True
    return False


def evaluate(user, argv):
    """
    Pure-Python decision function. Returns (ok: bool, reason: str).
    """
    from modules.api.data.permissions import check_path_access, check_write_access

    if not argv:
        return False, 'no rsync argv'

    is_sender, raw_paths = split_paths(argv)
    if raw_paths is None or not raw_paths:
        return False, 'could not locate path arguments'

    permission_check = check_path_access if is_sender else check_write_access

    for raw in raw_paths:
        rel = normalize(raw)
        if rel is None:
            return False, f'path escapes module root: {raw!r}'
        if not rel:
            return False, 'empty path'

        ok, reason = permission_check(user, rel)
        if not ok:
            return False, f'{reason} on {rel!r}'

        if is_sender:
            parts = PurePosixPath(rel).parts
            if len(parts) >= 2 and parts[0] == 'groups':
                group_name = parts[1]
                sub_parts = list(parts[2:])
                if has_descendant_deny(user, group_name, sub_parts):
                    return False, (
                        f'{rel!r} contains paths you cannot access; '
                        'narrow your request to a specific allowed file or subdirectory'
                    )

    return True, 'ok'


def _setup_django():
    import django
    sys.path.insert(0, '/app')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()


def main():
    _setup_django()

    from django.contrib.auth import get_user_model
    User = get_user_model()

    email = os.environ.get('RSYNC_USER_NAME', '').strip()
    if not email:
        sys.stderr.write('xrb-rsync-precheck: deny: missing RSYNC_USER_NAME\n')
        sys.exit(1)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        sys.stderr.write(f'xrb-rsync-precheck: deny: unknown user {email!r}\n')
        sys.exit(1)

    ok, reason = evaluate(user, read_argv_from_env())
    if not ok:
        sys.stderr.write(f'xrb-rsync-precheck: deny: {reason}\n')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
