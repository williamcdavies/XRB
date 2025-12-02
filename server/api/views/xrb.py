from rest_framework import viewsets

from api.models.xrb import XRB
from api.serializers.xrb import XRBSerializer

class XRBViewset(viewsets.ModelViewSet):
    queryset = XRB.objects.all()
    serializer_class = XRBSerializer