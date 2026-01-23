from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth                 import get_user_model
from rest_framework.decorators           import api_view, permission_classes
from rest_framework.permissions          import AllowAny

from modules.api.auth.serializers        import EmailSerializer

# entry point for user-authentication
@api_view(['POST'])
@permission_classes([AllowAny])
def start(request):
    # serialize start request:
    #   start requests are expected to be the key-value pair {'email': 'email.value'}.
    #   if start request cannot be appropriatley serialized a status.HTTP_400_BAD_REQUEST is 
    #       automatically raised.
    #   'email' field is read into email following validation 
    serializer = EmailSerializer(data=request.data)
    # Ref: https://www.django-rest-framework.org/api-guide/serializers/#validation
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    # normalise email for identity consistency
    email.strip().lower()

    # Ref: https://docs.djangoproject.com/en/6.0/ref/contrib/auth/
    User = get_user_model()
    # Ref: https://docs.djangoproject.com/en/6.0/ref/models/querysets/
    # lookup user by email:
    #   if user.email==email, User user=returned_user; bool created=False
    #   else,                 User user=returned_user; bool created=True
    user, user_created = User.objects.get_or_create(
        email=email,
        defaults={'username': email},
    )

    # Ref: https://django-otp-official.readthedocs.io/en/latest/_modules/django_otp/plugins/otp_email/models.html
    email_device, email_device_created = EmailDevice.objects.get_or_create(
        user=user,
        name='default',
        defaults={'email': email, 'confirmed': True},
    )
    
    
