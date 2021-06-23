from rest_framework import routers

from .views import UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'user', UserProfileViewSet)
urlpatterns = router.urls
