from rest_framework.routers import SimpleRouter

from .views import SearchViewSet

router = SimpleRouter()
router.register(r'search', SearchViewSet, basename="search-project")

urlpatterns = router.urls
