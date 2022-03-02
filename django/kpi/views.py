from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core.views import TokenAuthMixin
from .models import SolutionLog
from .serializers import SolutionLogSerializer, SolutionLogVerboseSerializer


class SolutionKPIViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    """
    View to retrieve Solutions KPIs
    """
    queryset = SolutionLog.objects.all()
    serializer_class = SolutionLogSerializer

    @swagger_auto_schema(responses={200: SolutionLogVerboseSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
