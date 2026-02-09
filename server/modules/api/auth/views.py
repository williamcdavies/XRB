from django_otp.plugins.otp_email.models import EmailDevice
from django.conf                         import settings
from django.contrib.auth                 import get_user_model
from rest_framework.decorators           import api_view, permission_classes
from rest_framework.permissions          import AllowAny
from rest_framework.response             import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens     import RefreshToken

from modules.api.auth.serializers        import CredentialSerializer
from modules.api.auth.serializers        import EmailSerializer


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # serialize login request:
    #   login requests are expected to be of the key-value pair {"email": "email.value"}.
    #   if login requests cannot be appropriately serialized, a status.HTTP_400_BAD_REQUEST is 
    #       automatically raised.
    #   'email' is read into email following validation 
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email'].strip().lower()

    # lookup user by email:
    #   if user.email==email, User user=returned_user
    #   else,                 User user=returned_user
    user, _ = User.objects.get_or_create(
        email=email,
        defaults={'username': email},
    )

    # lookup email_device by user and name (name because users may have > 1 email_device):
    #   if email_device.user==user 
    #   && email_device.name=='default, EmailDevice email_device=returned_email_device
    #   else,                           EmailDevice email_device=returned_email_device
    email_device, _ = EmailDevice.objects.get_or_create(
        user=user,
        name='default',
        defaults={'email': email, 'confirmed': True},
    )

    email_device.generate_challenge()

    return Response(status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):
    # serialize verify request:
    #   verify requests are expected to be of the key-value pairs {"email": "email.value"}, {"token": "token.value"}.
    #   if verify requests cannot be appropriately serialized, a status.HTTP_400_BAD_REQUEST is 
    #       automatically raised.
    #   'email' is read into email following validation 
    #   'token' is read into toekn following validation
    serializer = CredentialSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email'].strip().lower()
    token = serializer.validated_data['token']

    # lookup user by email:
    #   if user.email==email, User user=returned_user
    #   else,                 return 401 Unauthorized
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=401)
    
    # lookup email_device by user and name (name because users may have > 1 email_device):
    #   if email_device.user==user 
    #   && email_device.name=='default, EmailDevice email_device=returned_email_device
    #   else,                           return 401 Unauthorized
    try:
        email_device = EmailDevice.objects.get(
            user=user,
            name='default',
        )
    except EmailDevice.DoesNotExist:
        return Response(status=401)
    
    # verify token with email_device:
    #   if token is bad, return 401 Unauthorized
    if not email_device.verify_token(token):
        return Response(status=401)

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    
    response = Response({'access': str(access_token)})
    
    # ref: https://docs.djangoproject.com/en/6.0/ref/request-response/
    # store refresh token as httponly cookie:
    #   prevents refresh token from being read by client-side javascript
    # note:
    #   set secure=True  in prod
    #   set secure=False in dev
    response.delete_cookie('refresh_token', path='/', samesite='Lax')
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        path='/',
        secure=False,
        httponly=True,
        samesite='Lax'
    )

    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    old_refresh_token_str = request.COOKIES.get('refresh_token')
    
    # verify expired refresh token:
    #   if token is bad, return 401 Unauthorized
    if not old_refresh_token_str:
        return Response(status=401)

    # RefreshToken() can raise TokenError
    #   if token is bad, return 401 Unauthorized
    try:
        old_refresh_token = RefreshToken(old_refresh_token_str)
    except TokenError:
        return Response(status=401)
    
    # User.objects.get() can raise User.DoesNotExist
    #   if user is bad, return 401 Unauthorized
    try:
        user = User.objects.get(id=old_refresh_token.get('user_id'))
    except User.DoesNotExist:
        return Response(status=401)
    
    new_access_token = old_refresh_token.access_token
    new_refresh_token = RefreshToken.for_user(user)
    old_refresh_token.blacklist()
    
    response = Response({'access': str(new_access_token)})
    
    # ref: https://docs.djangoproject.com/en/6.0/ref/request-response/
    # store refresh token as httponly cookie:
    #   prevents refresh token from being read by client-side javascript
    # note:
    #   set secure=True  in prod
    #   set secure=False in dev
    response.delete_cookie('refresh_token', path='/', samesite='Lax')
    response.set_cookie(
        key='refresh_token',
        value=str(new_refresh_token),
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        path='/',
        secure=False,
        httponly=True,
        samesite='Lax'
    )

    return response