from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'preferred_avatar': user.preferred_avatar,
        'preferred_language': user.preferred_language,
        'type': user.type,
    })