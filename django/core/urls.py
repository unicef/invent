from django.conf.urls import url

from .views import StaticDataView

urlpatterns = [
    url(r'^static-data/$', view=StaticDataView.as_view(), name='static-data'),
]
