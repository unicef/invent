from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('solutions', views.SolutionKPIViewSet, base_name="solutions-kpi")
router.register('country-inclusion', views.CountryInclusionKPIViewSet, base_name="country-inclusion-kpi")

urlpatterns = router.urls
