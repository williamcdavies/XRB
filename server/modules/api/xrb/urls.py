from rest_framework.routers import DefaultRouter
from .views                 import XRBViewset

router = DefaultRouter()
router.register(r'', XRBViewset, basename='xrb')

urlpatterns = router.urls
