from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'import', views.ProjectImportV2ViewSet)
router.register(r'import-row', views.ImportRowViewSet)
router.register('software-request', views.TechnologyPlatformRequestViewSet)
router.register('hardware-request', views.HardwarePlatformRequestViewSet)
router.register('nontech-request', views.NontechPlatformRequestViewSet)
router.register('function-request', views.PlatformFunctionRequestViewSet)

urlpatterns = [
    path("projects/", include(router.urls)),
    path(r"projects/<int:pk>/",
         view=views.ProjectRetrieveViewSet.as_view({
             'get': 'retrieve',
         }),
         name="project-retrieve"),
    path(r"projects/<int:pk>/version-history",
         view=views.ProjectVersionHistoryViewSet.as_view({
             'get': 'retrieve',
         }),
         name="project-versions-retrieve"),
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
    path('projects/user-list/<str:list_name>/',
         view=views.ProjectListViewSet.as_view({
             'get': 'list'
         }), name="project-list"),
    path('projects/landing/',
         view=views.ProjectLandingBlocks.as_view({
             'get': 'list'
         }), name="project-landing"),
    path('projects/structure/',
        view=views.ProjectPublicViewSet.as_view({
            'get': 'project_structure'
        }),
        name="get-project-structure"),
    re_path(r"^projects/(?P<pk>\d+)/groups/$",
        view=views.ProjectGroupViewSet.as_view({
            'get': 'retrieve',
            'put': 'update'
        }),
        name="project-groups"),
    path('projects/map/',
        view=views.MapProjectCountryViewSet.as_view({
            'get': 'list',
        }),
        name="project-map"),
    path('projects/favorites/add/<int:pk>',
         view=views.ProjectModifyFavoritesViewSet.as_view({
             'put': 'add'
         }),
         name="projects-add-favorite"),
    path('projects/<int:pk>/image/',
         view=views.ProjectImageUploadViewSet.as_view({
             'put': 'update'
         }),
         name="projects-add-image"),
    path('projects/favorites/remove/<int:pk>',
         view=views.ProjectModifyFavoritesViewSet.as_view({
             'put': 'remove'
         }),
         name="projects-remove-favorite"),
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
    path("portfolio/active-list/",
        view=views.PortfolioActiveListViewSet.as_view({
            'get': 'list'
        }), name="portfolio-list-active"),
    path('portfolio/create/',
        view=views.PortfolioCreateViewSet.as_view({
            'post': 'create'
        }), name="portfolio-create"),
    path('portfolio/update/<int:pk>/',
         view=views.PortfolioUpdateViewSet.as_view({
             'put': 'update',
             'patch': 'partial_update'
         }),
         name="portfolio-update"),
    path('portfolio/manager-of/',
        view=views.PortfolioUserListViewSet.as_view({
            'get': 'list'
        }), name="portfolio-list"),
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
             'patch': 'partial_update'
         }), name='review-score-fill'),
    path('project-review/manager/<int:pk>/',
         view=views.ProjectPortfolioStateManagerViewSet.as_view({
             'get': 'retrieve',
             'post': 'update',
             'patch': 'partial_update'
         }), name='portfolio-project-manager-review'),
    path('country-manager-export/',
         view=views.CountryManagerExportView.as_view({
             'get': 'retrieve'
         }), name='country-manager-export'),
    path('problem-statement/',
         view=views.ProblemStatementListViewSet.as_view({
             'get': 'list'
         }), name='problem-statement-list'),
    path('solution/',
         view=views.SolutionListViewSet.as_view({
             'get': 'list'
         }), name='solution-list'),
    path(r"solutions/<int:pk>/",
         view=views.SolutionRetrieveViewSet.as_view({
             'get': 'retrieve',
         }),
         name="solution-retrieve"),
    path('solution/create/',
        view=views.SolutionCreateViewSet.as_view({
            'post': 'create'
        }), name="solution-create"),
    path(r'solution/update/<int:pk>/',
         view=views.SolutionUpdateViewSet.as_view({
             'put': 'update',
             'patch': 'partial_update'
         }),
         name="solution-update"),
    path(r'portfolio/<int:pk>/',
         view=views.PortfolioViewSet.as_view({
             'get': 'retrieve'
         }),
         name="portfolio-retrieve"),
]
