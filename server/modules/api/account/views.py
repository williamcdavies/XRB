from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'first_name':         user.first_name,
        'last_name':          user.last_name,
        'email':              user.email,
        'username':           user.username,
        'preferred_avatar':   user.preferred_avatar,
        'preferred_language': user.preferred_language,
        'type':               user.type,
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_name(request):
    user = request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name  = request.data.get('last_name',  user.last_name)
    user.save()
    return Response({'first_name': user.first_name, 'last_name': user.last_name})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_email(request):
    user = request.user
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
    user.email    = email
    user.username = email
    user.save()
    return Response({'email': user.email, 'username': user.username})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    user = request.user
    user.preferred_avatar = request.data.get('preferred_avatar', user.preferred_avatar)
    user.save()
    return Response({'preferred_avatar': user.preferred_avatar})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_language(request):
    user = request.user
    user.preferred_language = request.data.get('preferred_language', user.preferred_language)
    user.save()
    return Response({'preferred_language': user.preferred_language})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_type(request):
    user = request.user
    user.type = request.data.get('type', user.type)
    user.save()
    return Response({'type': user.type})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)