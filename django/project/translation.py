from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions
from .models import DigitalStrategy, HSCChallenge, HealthCategory, HealthFocusArea, InteroperabilityLink,\
    TechnologyPlatform, Licence, InteroperabilityStandard, HISBucket, HSCGroup


@register(DigitalStrategy)
class DigitalStrategyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HSCGroup)
class HSCGroupTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HSCChallenge)
class HSCChallengeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HealthCategory)
class HealthCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HealthFocusArea)
class HealthFocusAreaTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(InteroperabilityLink)
class InteroperabilityLinkTranslationOptions(TranslationOptions):
    fields = ('name', 'pre')


@register(TechnologyPlatform)
class TechnologyPlatformTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Licence)
class LicenceTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(InteroperabilityStandard)
class InteroperabilityStandardTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HISBucket)
class HISBucketTranslationOptions(TranslationOptions):
    fields = ('name',)
