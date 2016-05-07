from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer
)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        comment_list = Comment.objects.all()
        search_query = self.request.GET.get('search_query')
        if search_query:
            comment_list = comment_list.filter(
                Q(content__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            ).distinct()
        return comment_list


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type", "post")
        id = self.request.GET.get("id")
        parent_id = self.request.GET.get("parent_id")
        return create_comment_serializer(model_type=model_type,
                                         id=id,
                                         parent_id=parent_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    # lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'


# class CommentUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


# class CommentDeleteAPIView(DestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
