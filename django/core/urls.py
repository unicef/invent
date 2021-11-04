from django.conf.urls import url

from .views import StaticDataView, NewsFeedView

urlpatterns = [
    url(r'^static-data/$', view=StaticDataView.as_view(), name='static-data'),
    url(r'^news-feed/$', view=NewsFeedView.as_view({'get': 'list'}), name='news-feed'),
]
