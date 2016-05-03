from rest_framework import serializers

from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        # same as 'reverse' for urls
        view_name='posts-api:detail',
        lookup_field='pk'
    )
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'image',
            'user',
            'title',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image_url = obj.image.url
        except:
            image_url = None
        return image_url


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'user',
            'id',
            'image',
            'title',
            'slug',
            'content',
            'publish',
            'updated',
            'comments'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image_url = obj.image.url
        except:
            image_url = None
        return image_url

    def get_comments(self, obj):
        comments = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(comments, many=True).data
        return comments


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
            'updated'
        ]
