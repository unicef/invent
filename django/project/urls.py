from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'import', views.ProjectImportV2ViewSet)
router.register(r'import-row', views.ImportRowViewSet)

urlpatterns = [
    url(r"^projects/", include(router.urls)),
    url(r"^projects/(?P<pk>\d+)/$",
        view=views.ProjectRetrieveViewSet.as_view({
            'get': 'retrieve',
        }),
        name="project-retrieve"),
    path(r'projects/publish/<int:project_id>/<int:country_id>/',
         view=views.ProjectPublishViewSet.as_view({
             'put': 'update'
         }),
         name="project-publish"),
    path(r'projects/draft/<int:country_id>/',
         view=views.ProjectDraftViewSet.as_view({
             'post': 'create'
         }), name="project-create"),
    path(r'projects/draft/<int:project_id>/<int:country_id>/',
         view=views.ProjectDraftViewSet.as_view({
             'put': 'update'
         }),
         name="project-draft"),
    url(r"^projects/member-of/$",
        view=views.ProjectListViewSet.as_view({
            'get': 'list'
        }), name="project-list"),
    url(r"^projects/structure/$",
        view=views.ProjectPublicViewSet.as_view({
            'get': 'project_structure'
        }),
        name="get-project-structure"),
    url(r"^projects/structure/export/$",
        view=views.ProjectPublicViewSet.as_view({
            'get': 'project_structure_export'
        }),
        name="get-project-structure-export"),
    url(r"^projects/(?P<project_id>\d+)/version/$",
        view=views.ProjectVersionViewSet.as_view({
            'post': 'create'
        }),
        name="make-version"),
    url(r"^projects/(?P<project_id>\d+)/coverage/versions/$",
        view=views.ProjectVersionViewSet.as_view({
            'get': 'coverage_versions'
        }),
        name="get-coverage-versions"),
    url(r"^projects/(?P<project_id>\d+)/toolkit/versions/$",
        view=views.ProjectVersionViewSet.as_view({
            'get': 'toolkit_versions'
        }),
        name="get-toolkit-versions"),
    url(r"^projects/(?P<pk>\d+)/groups/$",
        view=views.ProjectGroupViewSet.as_view({
            'get': 'retrieve',
            'put': 'update'
        }),
        name="project-groups"),
    url(r"^projects/csv-export/$",
        view=views.CSVExportViewSet.as_view({
            'post': 'create'
        }), name="csv-export"),
    url(r"^projects/map/$",
        view=views.MapProjectCountryViewSet.as_view({
            'get': 'list',
        }),
        name="project-map"),
    path(r'approvals/<int:country_id>/',
         view=views.ProjectApprovalViewSet.as_view({
             'get': 'list'
         }),
         name="approval"),
    path(r'approval/<int:pk>/',
         view=views.ProjectApprovalViewSet.as_view({
             'put': 'update'
         }),
         name="approval"),
]
