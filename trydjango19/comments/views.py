from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect

from .models import Comment
from .forms import CommentForm


def comment_thread(request, comment_id):
    # obj = get_object_or_404(Comment, id=comment_id)
    obj = Comment.objects.filter(id=comment_id).first()

    initial_comment_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }

    comment_form = CommentForm(request.POST or None,
                               initial=initial_comment_data)

    if comment_form.is_valid():
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
        "comment": obj,
        "form": comment_form
    }
    return render(request, "comment_thread.html", context)
