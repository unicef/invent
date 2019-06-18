from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^projects/(?P<project_id>\d+)/toolkit/score/$",
        view=views.ToolkitViewSet.as_view({
            "post": "create"
        }),
        name="toolkit-scores"),
    url(r"^projects/(?P<project_id>\d+)/toolkit/data/$",
        view=views.ToolkitViewSet.as_view({
            "get": "retrieve"
        }),
        name="toolkit-data"),
]
