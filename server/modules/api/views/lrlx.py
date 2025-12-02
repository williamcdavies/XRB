from rest_framework import viewsets

from modules.api.models.lrlx import LRLX
from modules.api.serializers.lrlx import LRLXSerializer

class LRLXViewset(viewsets.ModelViewSet):
    queryset = LRLX.objects.all()
    serializer_class = LRLXSerializer