from django.urls import path
from .views import StaticDataView, NewsFeedView

urlpatterns = [
    path('static-data/', view=StaticDataView.as_view(), name='static-data'),
    path('news-feed/', view=NewsFeedView.as_view({'get': 'list'}), name='news-feed'),
]
