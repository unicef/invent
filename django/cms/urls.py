from rest_framework import routers

from cms.views import CmsViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register(r'cms', CmsViewSet)
router.register(r'comment', CommentViewSet)
urlpatterns = router.urls
