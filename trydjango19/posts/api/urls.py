from django.conf.urls import url

from posts.api.views import (
    PostListAPIView,
    PostDetailAPIView,
)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name="list"),
    # restframework treats pk as the default search value
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name="detail"),
    # url(r'^create/$', post_create),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name="update"),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name="delete"),
]
