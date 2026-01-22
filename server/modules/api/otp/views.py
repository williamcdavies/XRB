# api/views/otp.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    serializer = SendOTPSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    user = User.objects.get(email=email)
    
    # Create OTP
    otp = OTP.create_otp(user)
    
    # Send email
    try:
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP code is: {otp.code}\n\nThis code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'OTP sent successfully to your email',
            'email': email
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to send OTP email',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    otp_code = serializer.validated_data['otp']
    
    user = User.objects.get(email=email)
    
    # get the most recent unverified OTP
    try:
        otp = OTP.objects.filter(
            user=user,
            code=otp_code,
            is_verified=False
        ).latest('created_at')
        
        if not otp.is_valid():
            return Response({
                'error': 'OTP has expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark OTP as verified
        otp.is_verified = True
        otp.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'OTP verified successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
        
    except OTP.DoesNotExist:
        return Response({
            'error': 'Invalid OTP'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_with_otp(request):
    email = request.data.get('email')
    username = request.data.get('username')
    
    if not email or not username:
        return Response({
            'error': 'Email and username are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # check if user already exists
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'User with this email already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'Username already taken'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # create user without password
    user = User.objects.create_user(
        username=username,
        email=email,
        password=None
    )
    user.set_unusable_password() # prevents password-based login
    user.save()
    
    # create and send OTP
    otp = OTP.create_otp(user)
    
    try:
        send_mail(
            subject=f'Welcome {username}! Verify Your Email',
            message=f'Welcome to the UNR XRB platform!\n\nYour OTP code is: {otp.code}\n\nThis code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'User created successfully. OTP sent to email.',
            'email': email,
            'username': username
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        # If email fails, delete the user
        user.delete()
        return Response({
            'error': 'Failed to send OTP email',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)