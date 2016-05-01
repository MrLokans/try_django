from rest_framework import serializers

from posts.models import Post


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
            'updated'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image_url = obj.image.url
        except:
            image_url = None
        return image_url


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
            'updated'
        ]
