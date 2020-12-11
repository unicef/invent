from __future__ import unicode_literals

from modeltranslation.translator import register, TranslationOptions
from .models import DigitalStrategy, HSCChallenge, HealthCategory, HealthFocusArea, \
    TechnologyPlatform, HSCGroup, HardwarePlatform, NontechPlatform, PlatformFunction, Stage


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


@register(TechnologyPlatform)
class TechnologyPlatformTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(HardwarePlatform)
class HardwarePlatformTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(NontechPlatform)
class NontechPlatformTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(PlatformFunction)
class PlatformFunctionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Stage)
class StageTranslationOptions(TranslationOptions):
    fields = ('name',)
