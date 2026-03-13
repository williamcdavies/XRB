from rest_framework.decorators import api_view, permission_classes
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

#Email Change Authentication
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_change(request):
    new_email = request.data.get('email', '').strip().lower()
    if not new_email:
        return Response({'error': 'Email is required'}, status=400)

    email_device, _ = EmailDevice.objects.get_or_create(
        user=request.user,
        name='email_change',
        defaults={'email': new_email, 'confirmed': True},
    )
    email_device.email = new_email
    email_device.save()
    email_device.generate_challenge()

    return Response(status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_email_change(request):
    token = request.data.get('token', '')
    new_email = request.data.get('email', '').strip().lower()

    try:
        email_device = EmailDevice.objects.get(
            user=request.user,
            name='email_change',
        )
    except EmailDevice.DoesNotExist:
        return Response(status=401)

    if not email_device.verify_token(token):
        return Response(status=401)

    try:
        request.user.email = new_email
        request.user.username = new_email
        request.user.save()
    except IntegrityError:
        return Response({'error': 'An account with this email already exists.'}, status=400)

    try:
        login_device = EmailDevice.objects.get(user=request.user, name='default')
        login_device.email = new_email
        login_device.save()
    except EmailDevice.DoesNotExist:
        pass

    email_device.delete()
    return Response(status=200)

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
    email = request.data.get('email', '').strip()

    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_email(email)
    except ValidationError:
        return Response({'error': 'Enter a valid email address.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exclude(pk=user.pk).exists():
        return Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
    
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