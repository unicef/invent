from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions
from .models import NewsItem


@register(NewsItem)
class NewsItemTranslationOptions(TranslationOptions):
    fields = ('title', 'alt_text', 'link', 'link_text', 'description')
    empty_values = {'title': None}
