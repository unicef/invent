from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from cms.models import Post, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CmsSerializer(ModelSerializer):
    comments = SerializerMethodField()
    author_name = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('slug', 'state')

    @staticmethod
    def get_comments(post):
        comments = Comment.objects.filter(post=post).showable().order_by('-id')
        serializer = CommentSerializer(instance=comments, many=True)
        return serializer.data

    @staticmethod
    def get_author_name(post):
        return post.author.name
