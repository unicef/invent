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
    path(r'projects/publish/<int:project_id>/<int:country_office_id>/',
         view=views.ProjectPublishViewSet.as_view({
             'put': 'update'
         }),
         name="project-publish"),
    path(r'projects/unpublish/<int:project_id>/',
         view=views.ProjectUnPublishViewSet.as_view({
             'put': 'update'
         }),
         name="project-unpublish"),
    path(r'projects/publishaslatest/<int:project_id>/',
         view=views.ProjectPublishAsLatestViewSet.as_view({
             'get': 'update'
         }),
         name="project-publish-as-latest"),
    path(r'projects/draft/<int:country_office_id>/',
         view=views.ProjectDraftViewSet.as_view({
             'post': 'create'
         }), name="project-create"),
    path(r'projects/draft/<int:project_id>/<int:country_office_id>/',
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
    url(r"^projects/map/$",
        view=views.MapProjectCountryViewSet.as_view({
            'get': 'list',
        }),
        name="project-map"),
    path('projects/favorites/',
         view=views.ProjectFavoritesViewSet.as_view({
             'get': 'list'
         }),
         name="favorite-projects-list"),
    path('projects/favorites/add/',
         view=views.ProjectModifyFavoritesViewSet.as_view({
             'post': 'add'
         }),
         name="favorite-projects-add"),
    path('projects/favorites/remove/',
         view=views.ProjectModifyFavoritesViewSet.as_view({
             'post': 'remove'
         }),
         name="favorite-projects-remove"),
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
    url("portfolio/active-list/",
        view=views.PortfolioActiveListViewSet.as_view({
            'get': 'list'
        }), name="portfolio-list-active"),
    url('portfolio/create/',
        view=views.PortfolioCreateViewSet.as_view({
            'post': 'create'
        }), name="portfolio-create"),
    path('portfolio/update/<int:pk>/',
         view=views.PortfolioUpdateViewSet.as_view({
             'put': 'update',
             'patch': 'partial_update'
         }),
         name="portfolio-update"),
    url('portfolio/manager-of/',
        view=views.PortfolioUserListViewSet.as_view({
            'get': 'list'
        }), name="portfolio-list"),
    path('portfolio/<int:pk>/',
         view=views.PortfolioDetailedViewSet.as_view({
             'get': 'retrieve'
         }),
         name="portfolio-detailed"),
    path('portfolio/<int:pk>/add-project/',
         view=views.PortfolioProjectChangeReviewStatusViewSet.as_view({
             'post': 'move_from_inventory_to_review'
         }), name='portfolio-project-add'),
    path('portfolio/<int:pk>/remove-project/',
         view=views.PortfolioProjectChangeReviewStatusViewSet.as_view({
             'post': 'move_to_inventory'
         }), name='portfolio-project-remove'),
    path('portfolio/<int:pk>/approve-project/',
         view=views.PortfolioProjectChangeReviewStatusViewSet.as_view({
             'post': 'approve'
         }), name='portfolio-project-approve'),
    path('portfolio/<int:pk>/disapprove-project/',
         view=views.PortfolioProjectChangeReviewStatusViewSet.as_view({
             'post': 'disapprove'
         }), name='portfolio-project-disapprove'),
    path('portfolio/<int:pk>/projects/<str:project_filter>/',
         view=views.ProjectPortfolioListViewSet.as_view({
             'get': 'list'
         }),
         name="portfolio-project-list"),
    path('portfolio/<int:portfolio_id>/<int:project_id>/',
         view=views.PortfolioReviewAssignQuestionnaireViewSet.as_view({
             'post': 'create_questionnaire'
         }), name='portfolio-assign-questionnaire'),
    path('project-review/<int:pk>/',
         view=views.ReviewScoreAccessSet.as_view({
             'get': 'retrieve',
             'delete': 'destroy'
         }), name='review-score-get-or-delete'),
    path('project-review/<int:pk>/fill/',
         view=views.ReviewScoreAnswerViewSet.as_view({
             'post': 'update',
         }), name='review-score-fill'),
    path('project-review/manager/<int:pk>/',
         view=views.ProjectPortfolioStateManagerViewSet.as_view({
             'get': 'retrieve',
             'post': 'update'
         }), name='portfolio-project-manager-review')
]
