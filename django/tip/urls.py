from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.i18n import JSONCatalog
from rest_framework.documentation import include_docs_urls

admin.site.site_header = 'Digital Health Atlas'
API_TITLE = 'Digital Health Atlas API'
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
    urlpatterns.append(url(r'^api/docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)))
