from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.i18n import JSONCatalog
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from country.views import CountryOfficeViewSet, CountryLandingPageViewSet, CountryLandingListPageViewSet
from project.views import ProjectPublicViewSet

admin.site.site_header = 'UNICEF T4D & Innovation Inventory Portal'
API_TITLE = 'UNICEF T4D & Innovation Inventory Portal API'
API_DESCRIPTION = 'Private API'

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include("core.urls")),
    url(r"^api/", include("user.urls")),
    url(r"^api/", include("project.urls")),
    url(r"^api/", include("toolkit.urls")),
    url(r"^api/", include("country.urls")),
    url(r"^api/", include("search.urls")),
    url(r"^api/", include("cms.urls")),
    url(r"^api/", include("simple-feedback.urls")),
    url(r'^translation/json/$', JSONCatalog.as_view(), name='json-catalog'),
    url(r'^translation/', include('rosetta.urls'))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns.append(url(r'^api/devdocs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)))

api_info = openapi.Info(
    title='UNICEF T4D & Innovation Inventory Portal API',
    default_version='v1',
    description='UNICEF T4D & Innovation Inventory Portal API',
    contact=openapi.Contact(email="f@pulilab.com"),
)

api_info_router = SimpleRouter()
api_info_router.register(r'api/countryoffices', CountryOfficeViewSet, base_name='countryoffice')
api_info_router.register(r'api/landing-country', CountryLandingPageViewSet, base_name='landing-country'),
api_info_router.register(r'api/landing-country', CountryLandingListPageViewSet, base_name='landing-country'),

api_info_urlpatterns = [
    url(r"^api/", include("search.urls")),
    url(r"^api/projects/structure/",
        view=ProjectPublicViewSet.as_view({'get': 'project_structure'}),
        name="get-project-structure"),
]
api_info_urlpatterns += api_info_router.urls

api_schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=api_info_urlpatterns,
)

urlpatterns += [
    path('api/docs/', api_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
