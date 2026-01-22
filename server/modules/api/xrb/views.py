from rest_framework                     import viewsets

from .models      import XRB
from .serializers import XRBSerializer

class XRBViewset(viewsets.ModelViewSet):
    queryset = XRB.objects.all()
    serializer_class = XRBSerializer
    
    def get_queryset(self):
        queryset = XRB.objects.all()
        
        # if a name is provided in the query URL, filter using that
        name = self.request.query_params.get('name', None)
        
        if name is not None:
            queryset = queryset.filter(name=name)
            
        return queryset