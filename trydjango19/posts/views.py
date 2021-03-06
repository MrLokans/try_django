from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from django.utils import timezone

from comments.models import Comment
from comments.forms import CommentForm
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

    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    initial_comment_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }

    comments = Comment.objects.filter_by_instance(post)
    comment_form = CommentForm(request.POST or None,
                               initial=initial_comment_data)

    if comment_form.is_valid() and request.user.is_authenticated():
        cont_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=cont_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        cont_data = comment_form.cleaned_data.get('content')
        parent_obj = None

        try:
            parent_id = int(request.POST.get('parent_id'))
        except TypeError:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                        user=request.user,
                        content_type=content_type,
                        object_id=obj_id,
                        content=cont_data,
                        parent=parent_obj,
            )

        if created:
            print("New comment successfully created.")
        return redirect(new_comment.content_object.get_absolute_url())

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    # post_list = Post.objects.all().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.active()

    search_query = request.GET.get('search_query')
    if search_query:
        post_list = post_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        ).distinct()

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
