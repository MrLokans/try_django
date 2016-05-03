from django.conf.urls import url

from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name="list"),
    url(r'^(?P<comment_id>\d+)/$', CommentDetailAPIView.as_view(), name="thread"),
    # url(r'^(?P<comment_id>\d+)/delete/$', comment_delete, name="comment_delete)"),
]
