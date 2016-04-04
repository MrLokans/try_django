from django.db import models
from django.conf import settings

from posts.models import Post


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post = models.ForeignKey(Post)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return str(self.user.username)