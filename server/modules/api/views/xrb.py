from rest_framework import viewsets

from modules.api.models.xrb import XRB
from modules.api.serializers.xrb import XRBSerializer

class XRBViewset(viewsets.ModelViewSet):
    queryset = XRB.objects.all()
    serializer_class = XRBSerializer