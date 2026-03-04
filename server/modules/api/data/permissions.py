from pathlib import PurePosixPath


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
        if user.groups.filter(name=group_name).exists():
            return True, 'group_member'
        return False, 'not_group_member'

    return False, 'other'


def check_write_access(user, relative_path: str):
    parts = PurePosixPath(relative_path).parts

    if not parts:
        return False, 'empty_path'

    # any sort of file upload require user to be uploaded
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

    # groups/<groupname> — user must belong to the group
    if prefix == 'groups' and len(parts) >= 2:
        group_name = parts[1]
        if user.groups.filter(name=group_name).exists():
            return True, 'group_member'
        return False, 'not_group_member'

    return False, 'unmanaged_path'
