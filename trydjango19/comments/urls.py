from django.conf.urls import url

from .views import (
    comment_thread,
    comment_delete,
)

urlpatterns = [
    url(r'^(?P<comment_id>\d+)/$', comment_thread, name="comment_thread"),
    url(r'^(?P<comment_id>\d+)/delete/$', comment_delete, name="comment_delete"),
]
