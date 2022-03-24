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


class LanguagesSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    flag = serializers.CharField()


class SearchFilterSerializer(serializers.Serializer):
    name = serializers.CharField()
    displayName = serializers.CharField()
    value = serializers.BooleanField()


class LandingPageDefaultsSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    logo = serializers.BooleanField()
    cover = serializers.CharField()
    cover_text = serializers.CharField()
    footer_title = serializers.CharField()
    permanent_footer = serializers.CharField()
    footer_text = serializers.CharField()
    default_partners = serializers.ListField(child=serializers.CharField())
    partner_logos = serializers.ListField(child=serializers.CharField())


class SubLevelTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    displayName = serializers.CharField()


class NameIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TextIDSerializer(serializers.Serializer):
    id = serializers.CharField()
    text = serializers.CharField()


class LabelIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()


class StaticDataSerializer(serializers.Serializer):
    languages = LanguagesSerializer(many=True)
    search_filters = SearchFilterSerializer(many=True)
    landing_page_defaults = LandingPageDefaultsSerializer()
    sub_level_types = SubLevelTypeSerializer(many=True)
    unicef_regions = NameIDSerializer(many=True)
    dashboard_columns = LabelIDSerializer(many=True)
    partner_types = NameIDSerializer(many=True)
    link_types = NameIDSerializer(many=True)
    review_questions = serializers.DictField()
    scale_phases = NameIDSerializer(many=True)
    review_status = TextIDSerializer(many=True)
    solution_phases = NameIDSerializer(many=True, required=False)
    portfolio_status = TextIDSerializer(many=True)
