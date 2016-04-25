from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Comment
from .forms import CommentForm


@login_required(login_url='/login/')
def comment_delete(request, comment_id):

    try:
        obj = Comment.objects.get(id=int(comment_id))
    except ObjectDoesNotExist:
        print("Object with id {} is not found.".format(comment_id))
        raise Http404

    if obj.user != request.user:
        response = HttpResponse("You do not have permission to delete comment.")
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Successfully deleted comment")
        return redirect(parent_obj_url)

    context = {
        "comment": obj
    }

    return render(request, "confirm_comment_delete.html", context)


def comment_thread(request, comment_id):

    try:
        obj = Comment.objects.get(id=int(comment_id))
    except ObjectDoesNotExist:
        print("Object with id {} is not found.".format(comment_id))
        raise Http404

    # Refer to the thread start topic
    if not obj.is_parent:
        obj = obj.parent

    initial_comment_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }

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
        "comment": obj,
        "form": comment_form
    }
    return render(request, "comment_thread.html", context)
