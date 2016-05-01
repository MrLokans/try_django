from rest_framework import serializers

from posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        # same as 'reverse' for urls
        view_name='posts-api:detail',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'title',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish',
            'updated'
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
            'updated'
        ]
