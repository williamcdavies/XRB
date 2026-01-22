from rest_framework                      import viewsets

from modules.api.lrlx.models      import LRLX
from modules.api.lrlx.serializers import LRLXSerializer

class LRLXViewset(viewsets.ModelViewSet):
    queryset = LRLX.objects.all()
    serializer_class = LRLXSerializer
    
    def get_queryset(self):
        queryset = LRLX.objects.all()
        
        # if a name is provided in the query URL, filter using that
        name = self.request.query_params.get('name', None)
        
        if name is not None:
            queryset = queryset.filter(name=name)
            
        return queryset