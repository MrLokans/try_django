from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {"form": form}
    return render(request, "post_form.html", context)


def post_detail(request, post_id=None):

    post = get_object_or_404(Post, id=post_id)

    return render(request, "post_detail.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
