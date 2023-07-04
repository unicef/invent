from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('solutions', views.SolutionKPIViewSet, basename="solutions-kpi")
router.register('country-inclusion', views.CountryInclusionKPIViewSet, basename="country-inclusion-kpi")

urlpatterns = router.urls
