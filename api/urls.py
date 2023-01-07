from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('channels/', views.ChannelList.as_view()),
    path('channels/<int:channel_pk>/', views.ChannelDetail.as_view()),
    path('channels/<int:channel_pk>/contents/', views.ContentList.as_view()),
    path('channels/<int:channel_pk>/contents/<int:content_pk>/', views.ContentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
