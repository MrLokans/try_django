from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_create(request):
    return HttpResponse("<h1>Create</h1>")


def post_detail(request, id=None):

    post = get_object_or_404(Post, id=id)

    return render(request, "post_detail.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
