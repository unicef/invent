from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.views import CheckProjectAccessMixin, TeamTokenAuthMixin, get_object_or_400

from .serializers import ScoreSerializer
from .models import Toolkit


class ToolkitViewSet(TeamTokenAuthMixin, CheckProjectAccessMixin, GenericViewSet):
    serializer_class = ScoreSerializer

    @transaction.atomic
    def create(self, request, project_id):
        """
        Overrides create to insert and update Scores.
        """
        self.check_project_permission(request, project_id)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if there's a project for the ID.
            toolkit = get_object_or_400(
                Toolkit, select_for_update=True, error_message="No such project.", project=project_id)
            try:
                # Update the scores.
                toolkit.update_score(**serializer.validated_data)
            except IndexError:
                # Wrong index somewhere in the chain.
                return Response({"details": "No such answer."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, project_id):
        """
        Retrieves Toolkit data based on project_id.

        Args:
            project_id: ID for the given project.

        Returns:
            json: All the Toolkit data for the given project in JSON.
        """
        self.check_project_permission(request, project_id)

        toolkit = get_object_or_400(Toolkit, "No such project.", project=project_id)
        return Response(toolkit.data)
