from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.array import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel

from core.models import ExtendedModel, ExtendedMultilingualModel, SoftDeleteModel
from user.models import UserProfile


class LandingPageCommon(ExtendedMultilingualModel):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(blank=True, null=True)
    cover = models.ImageField(blank=True, null=True)
    cover_text = models.TextField(blank=True, null=True)
    footer_title = models.CharField(max_length=128, blank=True, null=True)
    footer_text = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def cover_url(self):
        return self.cover.url if self.cover else None

    @property
    def logo_url(self):
        return self.logo.url if self.logo else None


class UserManagement(models.Model):
    users = models.ManyToManyField(UserProfile, help_text="User/viewer who can read confidential answers", blank=True,
                                   related_name='%(class)s_viewers')
    admins = models.ManyToManyField(UserProfile, help_text="User who can write questionnaire", blank=True,
                                    related_name='%(class)s_admins')
    super_admins = models.ManyToManyField(UserProfile, help_text="User who can update landing and all above",
                                          blank=True, related_name='%(class)s_super_admins')

    class Meta:
        abstract = True

    def user_in_groups(self, profile):
        return self.admins.filter(id=profile.id).exists() or \
               self.super_admins.filter(id=profile.id).exists() or \
               self.users.filter(id=profile.id).exists()


class Country(UserManagement, LandingPageCommon):
    REGIONS = [
        (0, _('African Region')),
        (1, _('Region of the Americas')),
        (2, _('South-East Asia Region')),
        (3, _('European Region')),
        (4, _('Eastern Mediterranean Region')),
        (5, _('Western Pacific Region'))
    ]

    UNICEF_REGIONS = [
        (0, _('EAPR')),
        (1, _('ECAR')),
        (2, _('ESAR')),
        (3, _('LCAR')),
        (4, _('MENA')),
        (5, _('ROSA')),
        (6, _('WCAR')),
        (7, _('HQ'))
    ]

    code = models.CharField(max_length=4, default="NULL", help_text="ISO3166-1 country code", unique=True)
    region = models.IntegerField(choices=REGIONS, null=True, blank=True)
    map_data = JSONField(default=dict, blank=True)
    map_activated_on = models.DateTimeField(blank=True, null=True,
                                            help_text="WARNING: this field is for developers only")
    project_approval = models.BooleanField(default=False)
    lat = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=15)
    lon = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=15)

    unicef_region = models.IntegerField(choices=UNICEF_REGIONS, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ('id',)


class RegionalOffice(models.Model):
    name = models.CharField(max_length=256)


class CountryOffice(ExtendedModel):
    name = models.CharField(max_length=256)
    region = models.IntegerField(choices=Country.UNICEF_REGIONS, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return self.name


class FieldOffice(models.Model):
    name = models.CharField(max_length=256)
    country_office = models.ForeignKey(CountryOffice, blank=True, null=True, on_delete=models.CASCADE)


@receiver(pre_save, sender=Country)
def save_coordinates(sender, instance, **kwargs):
    if instance.map_data:
        try:
            instance.lat = instance.map_data['polylabel']['lat']
            instance.lon = instance.map_data['polylabel']['lng']
        except (TypeError, KeyError, ValueError):
            pass


class Donor(UserManagement, LandingPageCommon):
    code = models.CharField(max_length=10, default="NULL", help_text="Acronym for Donor", unique=True,
                            validators=[MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = "Donors"
        ordering = ('name',)


class PartnerLogo(ExtendedModel):
    country = models.ForeignKey(Country, related_name="partner_logos", on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    @property
    def image_url(self):
        return self.image.url if self.image else None


class DonorPartnerLogo(ExtendedModel):
    donor = models.ForeignKey(Donor, related_name="partner_logos", on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    @property
    def image_url(self):
        return self.image.url if self.image else None


class MapFile(ExtendedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='map_files')
    map_file = models.FileField(null=True, upload_to='uploaded_maps/')


class CustomQuestion(SoftDeleteModel, ExtendedModel, OrderedModel):
    TEXT = 1
    NUMBER = 2
    YESNO = 3
    SINGLE = 4
    MULTI = 5

    TYPE_CHOICES = (
        (TEXT, _("Text answer")),
        (NUMBER, _("Numeric answer")),
        (YESNO, _("Yes/No answer")),
        (SINGLE, _("Single choice")),
        (MULTI, _("Multiple choice")),
    )

    type = models.IntegerField(choices=TYPE_CHOICES, default=TEXT)
    question = models.CharField(max_length=256, blank=False)
    options = ArrayField(models.CharField(max_length=256), blank=True, null=True)

    private = models.BooleanField(default=False)
    required = models.BooleanField(default=False)

    class Meta:
        abstract = True
        default_manager_name = 'objects'
        base_manager_name = 'objects'


class DonorCustomQuestion(CustomQuestion):
    donor = models.ForeignKey(Donor, related_name='donor_questions', on_delete=models.CASCADE)
    order_with_respect_to = 'donor'

    class Meta(OrderedModel.Meta):
        pass

    def get_order(self):
        return self.__class__.objects.filter(donor=self.donor).values('id', 'order')


class CountryCustomQuestion(CustomQuestion):
    country = models.ForeignKey(Country, related_name='country_questions', on_delete=models.CASCADE)
    order_with_respect_to = 'country'

    class Meta(OrderedModel.Meta):
        pass

    def get_order(self):
        return self.__class__.objects.filter(country=self.country).values('id', 'order')
