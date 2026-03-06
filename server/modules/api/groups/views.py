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

User = get_user_model()

BASE_DATA_DIR = Path(os.environ.get('DATA_DIR', '/data'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    groups = request.user.groups.all().order_by('name')
    return Response({
        'groups': [
            {
                'id': g.id,
                'name': g.name,
                'member_count': g.user_set.count(),
            }
            for g in groups
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
    try:
        group = request.user.groups.get(id=group_id)
    except AuthGroup.DoesNotExist:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    members = group.user_set.all().order_by('email')
    return Response({
        'id': group.id,
        'name': group.name,
        'members': [
            {
                'id': m.id,
                'email': m.email,
                'first_name': m.first_name,
                'last_name': m.last_name,
            }
            for m in members
        ],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, group_id):
    try:
        group = request.user.groups.get(id=group_id)
    except AuthGroup.DoesNotExist:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
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

    if group.user_set.filter(id=user_to_add.id).exists():
        return Response(
            {'error': 'User is already a member of this group'},
            status=status.HTTP_409_CONFLICT,
        )

    user_to_add.groups.add(group)

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
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, group_id, user_id):
    try:
        group = request.user.groups.get(id=group_id)
    except AuthGroup.DoesNotExist:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        user_to_remove = group.user_set.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User is not a member of this group'},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_to_remove.groups.remove(group)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, group_id):
    try:
        group = request.user.groups.get(id=group_id)
    except AuthGroup.DoesNotExist:
        return Response(
            {'error': 'Group not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    group.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
