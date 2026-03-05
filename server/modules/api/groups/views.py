import os
from pathlib import Path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as AuthGroup

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
