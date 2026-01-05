from django.contrib.auth.models      import User
from rest_framework                  import status
from rest_framework.authtoken.views  import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators       import api_view, permission_classes
from rest_framework.permissions      import AllowAny, IsAuthenticated
from rest_framework.response         import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'})