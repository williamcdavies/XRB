from django_otp.plugins.otp_email.models import EmailDevice
from django.conf                         import settings
from django.contrib.auth                 import get_user_model
from rest_framework.decorators           import api_view, permission_classes
from rest_framework.permissions          import AllowAny
from rest_framework.response             import Response
from rest_framework_simplejwt.tokens     import RefreshToken

from modules.api.auth.serializers        import CredentialSerializer
from modules.api.auth.serializers        import EmailSerializer


# entry point for user-authentication
@api_view(['POST'])
@permission_classes([AllowAny])
def start(request):
    # serialize start request:
    #   start requests are expected to be of the key-value pair {"email": "email.value"}.
    #   if start requests cannot be appropriately serialized, a status.HTTP_400_BAD_REQUEST is 
    #       automatically raised.
    #   'email' is read into email following validation 
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email'].strip().lower()

    User = get_user_model()
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

    return Response()


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

    User = get_user_model()
    # lookup user by email:
    #   if user.email==email, User user=returned_user
    #   else,                 return 401 Unauthorized
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'detail': 'Unverifiable credentials'},
            status=401,
        )
    
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
        return Response(
            {'detail': 'Unverifiable credentials'},
            status=401,
        )
    
    # verify token with email_device
    #   if token is unverifiable, return 401 Unauthorized
    if not email_device.verify_token(token):
        return Response(
            {'detail': 'Unverifiable credentials'},
            status=401,
        )

    refresh  = RefreshToken.for_user(user)
    access   = refresh.access_token
    response = Response({'access': str(access)})
    
    # ref: https://docs.djangoproject.com/en/6.0/ref/request-response/
    # set response cookie
    response.set_cookie(
        key='refresh',
        value=str(refresh),
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        path='api/auth/refresh/',
        # ! IMPORTANT !
        # set secure=True in production
        #   tokens will not be encryped if secure=False
        secure=False,
        # ! IMPORTANT !
        httponly=True,
        samesite='Strict'
    )

    return response