from rest_framework import serializers

from core.models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = ('id', 'order', 'title', 'description', 'alt_text', 'link', 'link_text', 'thumbnail')

    @staticmethod
    def get_thumbnail(obj):
        return obj.thumbnail.url if obj.thumbnail else None
