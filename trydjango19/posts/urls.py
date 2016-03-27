from django.conf.urls import url

from .views import (
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete
)

urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', post_create),
    url(r'^(?P<post_id>\d+)/$', post_detail, name="detail"),
    url(r'^update/$', post_update),
    url(r'^delete/$', post_delete),
]
