from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions
from .models import Country, Donor


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)
    empty_values = {'name': None}


@register(Donor)
class DonorTranslationOptions(TranslationOptions):
    fields = ('name',)
    empty_values = {'name': None}
