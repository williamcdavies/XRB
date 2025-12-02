from rest_framework import viewsets

from api.models.lrlx import LRLX
from api.serializers.lrlx import LRLXSerializer

class LRLXViewset(viewsets.ModelViewSet):
    queryset = LRLX.objects.all()
    serializer_class = LRLXSerializer