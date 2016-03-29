import os

from django.db import models
from django.core.urlresolvers import reverse


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # path = os.path.join(instance.id, instance.id)
    # path = ".".join(path, extension)
    path = os.path.join(instance.id, filename)
    return path


class Post(models.Model):

    class Meta:
        ordering = ["timestamp", "-updated"]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={'post_id': self.id})
