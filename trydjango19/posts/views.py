from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Post
from .forms import PostForm


def post_create(request):

    if not request.user.is_authenticated():
        raise Http404

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "Post successfull created.")
        return redirect(post.get_absolute_url())
    context = {"form": form}
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):

    post = get_object_or_404(Post, slug=slug)
    context = {
        "post": post,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    post_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(post_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var, 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "post_list.html", {"posts": posts,
                                              "page_request_var": "page"})


def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Post successfull saved.")
        return redirect(post.get_absolute_url())
    context = {
        "post": post,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Post successfull deleted.")
    return redirect("posts:list")
