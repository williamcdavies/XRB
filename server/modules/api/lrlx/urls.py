from rest_framework.routers import DefaultRouter
from .views                 import LRLXViewset

router = DefaultRouter()
router.register(r'', LRLXViewset, basename='lrlx')

urlpatterns = router.urls
