from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth                 import get_user_model
from rest_framework.decorators           import api_view, permission_classes
from rest_framework.permissions          import AllowAny
from rest_framework.response             import Response

from modules.api.auth.serializers        import EmailSerializer

# entry point for user-authentication
@api_view(['POST'])
@permission_classes([AllowAny])
def start(request):
    # serialize start request:
    #   start requests are expected to be of the key-value pair {'email': 'email.value'}.
    #   if start requests cannot be appropriately serialized, a status.HTTP_400_BAD_REQUEST is 
    #       automatically raised.
    #   'email' is read into email following validation 
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    email = email.strip().lower()

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

    token = email_device.generate_token()
    email_device.send_mail(token)

    return Response()