from pathlib import PurePosixPath

from modules.api.groups.models import FileAccessControl, GroupMembership


def _check_group_file_access(user, group_name, subpath_parts):
    """
    cekcs per-file access control for the given user
    """
    from django.contrib.auth.models import Group as AuthGroup

    try:
        group = AuthGroup.objects.get(name=group_name)
    except AuthGroup.DoesNotExist:
        return False, 'group_not_found'

    # Admins bypass file-level restrictions
    is_admin = GroupMembership.objects.filter(
        user=user, group=group, role=GroupMembership.ROLE_ADMIN,
    ).exists()
    if is_admin:
        return True, 'group_admin'

    # check heirarchy to see if block happens further up
    paths_to_check = []
    for i in range(len(subpath_parts), 0, -1):
        paths_to_check.append('/'.join(subpath_parts[:i]))

    restrictions = FileAccessControl.objects.filter(
        group=group, path__in=paths_to_check,
    )

    if not restrictions.exists():
        return True, 'group_member'

    # most specific (longest) matching restriction wins
    restriction_map = {r.path: r for r in restrictions}
    for p in paths_to_check:
        if p in restriction_map:
            if restriction_map[p].allowed_users.filter(id=user.id).exists():
                return True, 'file_access_granted'
            return False, 'file_access_denied'

    return True, 'group_member'


def filter_group_items(user, group_name, items):
    """
    filters list of items user can see in group
    """
    from django.contrib.auth.models import Group as AuthGroup

    try:
        group = AuthGroup.objects.get(name=group_name)
    except AuthGroup.DoesNotExist:
        return items

    is_admin = GroupMembership.objects.filter(
        user=user, group=group, role=GroupMembership.ROLE_ADMIN,
    ).exists()
    if is_admin:
        return items

    restrictions = {
        r.path: r
        for r in FileAccessControl.objects.filter(group=group).prefetch_related('allowed_users')
    }
    if not restrictions:
        return items

    filtered = []
    for item in items:
        # item['path'] is like "groups/<name>/subdir/file.csv"
        item_parts = PurePosixPath(item['path']).parts
        # subpath within the group dir (everything after "groups/<name>")
        if len(item_parts) <= 2:
            filtered.append(item)
            continue

        # Check this path and all ancestor paths for restrictions
        sub_parts = item_parts[2:]
        blocked = False
        for i in range(len(sub_parts), 0, -1):
            candidate = '/'.join(sub_parts[:i])
            if candidate in restrictions:
                if not restrictions[candidate].allowed_users.filter(id=user.id).exists():
                    blocked = True
                break  # most specific match wins

        if not blocked:
            filtered.append(item)

    return filtered


def check_path_access(user, relative_path: str):
    parts = PurePosixPath(relative_path).parts  # e.g. ('public', 'file.csv')

    if not parts:
        return False, 'empty_path'

    prefix = parts[0]

    # public
    if prefix == 'public':
        return True, 'public'

    # everything below needs some sort of authentication
    if not user or not user.is_authenticated:
        return False, 'authentication_required'

    # users/ root or users/<email>
    if prefix == 'users':
        if len(parts) == 1:
            return True, 'users_root'
        owner_email = parts[1]
        if user.email == owner_email:
            return True, 'owner'
        return False, 'not_owner'

    # groups/<groupname> — user must belong to the group
    if prefix == 'groups' and len(parts) >= 2:
        group_name = parts[1]
        if not user.groups.filter(name=group_name).exists():
            return False, 'not_group_member'
        # If there are deeper path segments, check file-level access
        if len(parts) > 2:
            return _check_group_file_access(user, group_name, parts[2:])
        return True, 'group_member'

    return False, 'other'


def check_write_access(user, relative_path: str):
    parts = PurePosixPath(relative_path).parts

    if not parts:
        return False, 'empty_path'

    # any sort of file upload require user to be authenticated
    if not user or not user.is_authenticated:
        return False, 'authentication_required'

    prefix = parts[0]

    # any authenticated user can upload to public
    if prefix == 'public':
        return True, 'public'

    # uploading to own directory
    if prefix == 'users' and len(parts) >= 2:
        owner_name = parts[1]
        if user.email == owner_name:
            return True, 'owner'
        return False, 'not_owner'

    # groups/<groupname> — user must belong to the group + file-level check
    if prefix == 'groups' and len(parts) >= 2:
        group_name = parts[1]
        if not user.groups.filter(name=group_name).exists():
            return False, 'not_group_member'
        if len(parts) > 2:
            return _check_group_file_access(user, group_name, parts[2:])
        return True, 'group_member'

    return False, 'unmanaged_path'
