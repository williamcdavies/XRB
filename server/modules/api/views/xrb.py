from rest_framework import viewsets


from modules.api.models.xrb      import XRB
from modules.api.serializers.xrb import XRBSerializer


class XRBViewset(viewsets.ModelViewSet):
    queryset         = XRB.objects.all()
    serializer_class = XRBSerializer
    
    def get_queryset(self):
        queryset = XRB.objects.all()
        
        # if a name is provided in the query URL, filter by name
        name = self.request.query_params.get('name', None)
        
        if name is not None:
            queryset = queryset.filter(name=name)
            
        return queryset