from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import serializers

from comments.models import Comment

User = get_user_model()


def create_comment_serializer(model_type='post', id=None, parent_id=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'parent',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.type = model_type
            self.id = id
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super().__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.object.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.Validationerror("Invalid content type.")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.Validationerror("Invalid content type id.")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(model_type, id,
                                                           user, content,
                                                           parent_obj=parent_obj)
            return comment


    return CommentCreateSerializer


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'content',
            'object_id',
            'reply_count',
            'parent'
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'object_id',
            'timestamp',
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'content',
            'object_id',
            'timestamp',
            'replies',
            'reply_count'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
