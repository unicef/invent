from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('solutions', views.SolutionKPIViewSet, base_name="solutions-kpi")

urlpatterns = router.urls
