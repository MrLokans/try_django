from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    def all(self):
        """Only comments with no parents are rendered"""
        qs = super().filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        comments = super().filter(content_type=content_type,
                                  object_id=object_id).filter(parent=None)
        return comments


class Comment(models.Model):

    class Meta:
        ordering = ['-timestamp', ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()

    parent = models.ForeignKey("self", null=True, blank=True)

    objects = CommentManager()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    def children(self):
        children = Comment.objects.filter(parent=self)
        return children

    def get_absolute_url(self):
        return reverse("comments:comment_thread",
                       kwargs={"comment_id": self.id})

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
