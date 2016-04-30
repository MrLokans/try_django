from django.conf.urls import url

from posts.api.views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name="list"),
    # restframework treats pk as the default search value
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name="detail"),
    # url(r'^create/$', post_create),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateAPIView.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteAPIView.as_view(), name="delete"),
]
