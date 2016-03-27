from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Post successfull created.")
        return HttpResponseRedirect(post.get_absolute_url())
    else:
        messages.error(request, "Post creation error.")
    context = {"form": form}
    return render(request, "post_form.html", context)


def post_detail(request, post_id=None):

    post = get_object_or_404(Post, id=post_id)

    return render(request, "post_detail.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})


def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Post successfull saved.")
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        "post": post,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post successfull deleted.")
    return redirect("posts:list")
