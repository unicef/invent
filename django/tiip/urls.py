from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path
from django.views.i18n import JSONCatalog
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from core.views import StaticDataView
from country.views import CountryOfficeViewSet, CountryLandingPageViewSet, CountryLandingListPageViewSet
from kpi.views import SolutionKPIViewSet, CountryInclusionKPIViewSet
from project.views import ProjectPublicViewSet, PortfolioActiveListViewSet, ProblemStatementListViewSet, \
    SolutionListViewSet
from user.views import OrganisationViewSet

admin.site.site_header = settings.PROJECT_NAME
API_TITLE = f'{settings.PROJECT_NAME} API'
API_DESCRIPTION = 'Private API'

urlpatterns = [
    url(r'^account/', include('allauth.urls')),
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include("azure_services.urls")),
    url(r"^api/", include("core.urls")),
    url(r"^api/", include("user.urls")),
    url(r"^api/", include("project.urls")),
    url(r"^api/", include("country.urls")),
    url(r"^api/", include("search.urls")),
    url(r"^api/", include("simple-feedback.urls")),
    url(r"^api/kpi/", include("kpi.urls")),
    url(r'^translation/json/$', JSONCatalog.as_view(), name='json-catalog'),
    url(r'^translation/', include('rosetta.urls')),
    url(r'^health_check/', include('health_check.urls'))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns.append(url(r'^api/devdocs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)))

api_info = openapi.Info(
    title=API_TITLE,
    default_version='v1',
    description=API_TITLE,
    contact=openapi.Contact(email=settings.API_MAINTAINER),
)

api_info_router = SimpleRouter()
api_info_router.register('api/countryoffices', CountryOfficeViewSet, base_name='countryoffice')
api_info_router.register('api/landing-country', CountryLandingPageViewSet, base_name='landing-country'),
api_info_router.register('api/landing-country', CountryLandingListPageViewSet, base_name='landing-country'),
api_info_router.register('api/organisations', OrganisationViewSet, base_name='organisation')
api_info_router.register('api/kpi/solutions', SolutionKPIViewSet, base_name="solutions-kpi")
api_info_router.register('api/kpi/country-inclusion', CountryInclusionKPIViewSet, base_name="country-inclusion-kpi")

api_info_urlpatterns = [
    path("api/", include("search.urls")),
    path("api/projects/structure/",
         view=ProjectPublicViewSet.as_view({'get': 'project_structure'}),
         name="get-project-structure"),
    path("api/portfolio/active-list/",
         view=PortfolioActiveListViewSet.as_view({'get': 'list'}),
         name="portfolio-list-active"),
    path('api/static-data/', view=StaticDataView.as_view(),
         name='static-data'),
    path('api/problem-statement/',
         view=ProblemStatementListViewSet.as_view({'get': 'list'}),
         name='problem-statement-list'),
    path('api/solution/',
         view=SolutionListViewSet.as_view({'get': 'list'}),
         name='solution-list'),
]
api_info_urlpatterns += api_info_router.urls

api_schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=api_info_urlpatterns,
)

urlpatterns += [
    path('api/docs/', api_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'api/swagger(?P<format>\.json|\.yaml)$', api_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', api_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]