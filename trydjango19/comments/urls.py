from django.conf.urls import url

from .views import (
    comment_thread,
)

urlpatterns = [
    url(r'^(?P<comment_id>\d+)/$', comment_thread, name="comment_thread"),
    # url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete, name="delete"),
]
