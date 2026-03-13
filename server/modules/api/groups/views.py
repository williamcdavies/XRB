import os
from pathlib import Path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as AuthGroup
from django.core.mail import send_mail

from .models import GroupMembership

User = get_user_model()

BASE_DATA_DIR = Path(os.environ.get('DATA_DIR', '/data'))


def _get_membership(user, group_id):
    """Return (group, membership) or None if the user is not a member."""
    try:
        membership = GroupMembership.objects.select_related('group').get(
            user=user, group_id=group_id,
        )
        return membership.group, membership
    except GroupMembership.DoesNotExist:
        return None, None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    memberships = GroupMembership.objects.filter(user=request.user).select_related('group').order_by('group__name')
    return Response({
        'groups': [
            {
                'id': m.group.id,
                'name': m.group.name,
                'member_count': m.group.memberships.count(),
            }
            for m in memberships
        ]
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    name = (request.data.get('name') or '').strip()
    if not name:
        return Response(
            {'error': 'Missing required parameter: name'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if '/' in name or '\\' in name:
        return Response(
            {'error': 'Group name must not contain slashes'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if AuthGroup.objects.filter(name=name).exists():
        return Response(
            {'error': 'A group with that name already exists'},
            status=status.HTTP_409_CONFLICT,
        )

    group = AuthGroup.objects.create(name=name)
    request.user.groups.add(group)
    GroupMembership.objects.create(
        user=request.user, group=group, role=GroupMembership.ROLE_ADMIN,
    )

    group_dir = BASE_DATA_DIR / 'groups' / name
    group_dir.mkdir(parents=True, exist_ok=True)

    return Response({
        'id': group.id,
        'name': group.name,
        'member_count': 1,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_detail(request, group_id):
    group, membership = _get_membership(request.user, group_id)
    if group is None:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    memberships = group.memberships.select_related('user').order_by('user__email')
    return Response({
        'id': group.id,
        'name': group.name,
        'current_user_role': membership.role,
        'members': [
            {
                'id': m.user.id,
                'email': m.user.email,
                'first_name': m.user.first_name,
                'last_name': m.user.last_name,
                'role': m.role,
            }
            for m in memberships
        ],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, group_id):
    group, membership = _get_membership(request.user, group_id)
    if group is None:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if membership.role != GroupMembership.ROLE_ADMIN:
        return Response(
            {'error': 'Only admins can add members'},
            status=status.HTTP_403_FORBIDDEN,
        )

    email = (request.data.get('email') or '').strip()
    if not email:
        return Response(
            {'error': 'Missing required parameter: email'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user_to_add = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': f'No user found with email: {email}'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if group.memberships.filter(user=user_to_add).exists():
        return Response(
            {'error': 'User is already a member of this group'},
            status=status.HTTP_409_CONFLICT,
        )

    user_to_add.groups.add(group)
    GroupMembership.objects.create(
        user=user_to_add, group=group, role=GroupMembership.ROLE_USER,
    )

    try:
        send_mail(
            subject=f'You have been added to "{group.name}"',
            message=(
                f'Hi,\n\n'
                f'{request.user.email} has added you to the group "{group.name}".\n\n'
                f'You now have access to the group\'s shared files.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_to_add.email],
            fail_silently=True,
        )
    except Exception:
        pass

    return Response({
        'id': user_to_add.id,
        'email': user_to_add.email,
        'first_name': user_to_add.first_name,
        'last_name': user_to_add.last_name,
        'role': GroupMembership.ROLE_USER,
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, group_id, user_id):
    group, membership = _get_membership(request.user, group_id)
    if group is None:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Non-admins can only remove themselves
    if membership.role != GroupMembership.ROLE_ADMIN and user_id != request.user.id:
        return Response(
            {'error': 'Only admins can remove other members'},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        target_membership = group.memberships.select_related('user').get(user_id=user_id)
    except GroupMembership.DoesNotExist:
        return Response(
            {'error': 'User is not a member of this group'},
            status=status.HTTP_404_NOT_FOUND,
        )

    target_membership.user.groups.remove(group)
    target_membership.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_role(request, group_id, user_id):
    group, membership = _get_membership(request.user, group_id)
    if group is None:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if membership.role != GroupMembership.ROLE_ADMIN:
        return Response(
            {'error': 'Only admins can change roles'},
            status=status.HTTP_403_FORBIDDEN,
        )

    role = request.data.get('role')
    if role not in (GroupMembership.ROLE_ADMIN, GroupMembership.ROLE_USER):
        return Response(
            {'error': 'Invalid role. Must be "admin" or "user"'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user_id == request.user.id:
        return Response(
            {'error': 'You cannot change your own role'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        target_membership = group.memberships.get(user_id=user_id)
    except GroupMembership.DoesNotExist:
        return Response(
            {'error': 'User is not a member of this group'},
            status=status.HTTP_404_NOT_FOUND,
        )

    target_membership.role = role
    target_membership.save()
    return Response({
        'id': user_id,
        'role': role,
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, group_id):
    group, membership = _get_membership(request.user, group_id)
    if group is None:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if membership.role != GroupMembership.ROLE_ADMIN:
        return Response(
            {'error': 'Only admins can delete groups'},
            status=status.HTTP_403_FORBIDDEN,
        )

    group.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
