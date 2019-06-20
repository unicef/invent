from typing import Union

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.dateformat import format
from django.db.transaction import atomic
from django.template import loader
from django.core.mail import send_mail
from django.core import management
from django.utils.translation import ugettext, override
from django.conf import settings

from user.models import UserProfile
from .models import Country, Donor, PartnerLogo, DonorPartnerLogo, MapFile, \
    DonorCustomQuestion, CountryCustomQuestion, CustomQuestion


class OptionsValidatorMixin:
    def validate_options_for_choice_fields(self, value):
        if not len(value) > 0:
            raise ValidationError({'options': 'Ensure options field has at least 1 elements.'})

    def validate(self, attrs):
        if attrs.get('type', CustomQuestion.TEXT) in (CustomQuestion.SINGLE, CustomQuestion.MULTI):
            self.validate_options_for_choice_fields(attrs['options'])
        return attrs


class CountryCustomQuestionSerializer(OptionsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = CountryCustomQuestion
        fields = "__all__"


class DonorCustomQuestionSerializer(OptionsValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = DonorCustomQuestion
        fields = "__all__"


class PartnerLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerLogo
        fields = ("id", "country", "image", "image_url",)
        read_only_fields = ("image_url",)


class DonorPartnerLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorPartnerLogo
        fields = ("id", "donor", "image", "image_url",)
        read_only_fields = ("image_url",)


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name')


class MapFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapFile
        fields = ('id', 'country', 'map_file',)


class AtomicUpdate:
    @atomic
    def update(self, instance, validated_data):
        # Select for update to avoid race conditions caused by partial update
        # https://github.com/encode/django-rest-framework/issues/4675
        instance = self.Meta.model.objects.select_for_update().get(pk=instance.id)
        # perform update
        return super().update(instance, validated_data)


class CountryImageSerializer(AtomicUpdate, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'logo', 'logo_url', 'cover', 'cover_url')
        read_only_fields = ('logo_url', "cover_url")


class DonorImageSerializer(AtomicUpdate, serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('id', 'logo', 'logo_url', 'cover', 'cover_url')
        read_only_fields = ('logo_url', "cover_url")


class UpdateAdminMixin:
    @atomic
    def update(self, instance, validated_data):
        # keep original lists for comparison
        original_users = set(instance.users.all().only('id'))
        original_admins = set(instance.admins.all().only('id'))
        original_super_admins = set(instance.super_admins.all().only('id'))

        # Select for update to avoid race conditions caused by partial update
        # https://github.com/encode/django-rest-framework/issues/4675
        instance = self.Meta.model.objects.select_for_update().get(pk=instance.id)
        # perform update
        instance = super().update(instance, validated_data)

        # figure out the new entities
        new_users = set(instance.users.all().only('id')) - original_users
        new_admins = set(instance.admins.all().only('id')) - original_admins
        new_super_admins = set(instance.super_admins.all().only('id')) - original_super_admins

        # remove new additions from any other user group
        if new_users:
            instance.admins.remove(*new_users)
            instance.super_admins.remove(*new_users)
            self.notify_users(new_users, instance, ugettext('Viewer'))

        if new_admins:
            instance.users.remove(*new_admins)
            instance.super_admins.remove(*new_admins)
            self.notify_users(new_admins, instance, ugettext('Admin'))

        if new_super_admins:
            instance.users.remove(*new_super_admins)
            instance.admins.remove(*new_super_admins)
            self.notify_users(new_super_admins, instance, ugettext('System Admin'))

        return instance

    def notify_users(self, user_profiles, instance, group):
        html_template = loader.get_template('email/master-inline.html')
        for profile in user_profiles:
            with override(profile.language):
                subject = "Notification: You have been selected as {} for {}".format(group, instance.name)
                subject = ugettext(subject)
                model_name = self.Meta.model.__name__.lower()
                html_message = html_template.render({'type': '{}_admin'.format(model_name),
                                                     'group': group,
                                                     'full_name': profile.name,
                                                     '{}_name'.format(model_name): instance.name,
                                                     'language': profile.language})

            send_mail(
                subject=subject,
                message="",
                from_email=settings.FROM_EMAIL,
                recipient_list=[profile.user.email],
                html_message=html_message,
                fail_silently=True)


def can_read_private_questions(obj: Union[Country, Donor], request) -> bool:
    return request.user.is_superuser or obj.user_in_groups(request.user.userprofile)


COUNTRY_FIELDS = ("id", "name", "code", "logo", "logo_url", "cover", "cover_url", "cover_text", "footer_title",
                  "footer_text", "partner_logos", "project_approval", "map_data", "map_version", "map_files",
                  "map_activated_on", "country_questions", "lat", "lon")
READ_ONLY_COUNTRY_FIELDS = ("name", "code", "logo", "logo_url", "cover", "cover_url", "map_version", "map_files",
                            "map_activated_on", "country_questions", "lat", "lon")
COUNTRY_ADMIN_FIELDS = ('user_requests', 'admin_requests', 'super_admin_requests',)
READ_ONLY_COUNTRY_ADMIN_FIELDS = ("cover_text", "footer_title", "footer_text", "partner_logos", "project_approval",)


class SuperAdminCountrySerializer(UpdateAdminMixin, serializers.ModelSerializer):
    partner_logos = PartnerLogoSerializer(many=True, read_only=True)
    country_questions = serializers.SerializerMethodField()
    map_version = serializers.SerializerMethodField()
    map_files = MapFileSerializer(many=True, read_only=True)
    user_requests = serializers.SerializerMethodField()
    admin_requests = serializers.SerializerMethodField()
    super_admin_requests = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = COUNTRY_FIELDS + COUNTRY_ADMIN_FIELDS + ('users', 'admins', 'super_admins',)
        read_only_fields = READ_ONLY_COUNTRY_FIELDS + COUNTRY_ADMIN_FIELDS

    def update(self, instance, validated_data):
        map_changed = 'map_data' in validated_data and instance.map_data != validated_data['map_data']
        instance = super().update(instance, validated_data)
        if map_changed:
            management.call_command('clean_maps', instance.code)
        return instance

    def get_map_version(self, obj):
        if obj.map_activated_on:
            return format(obj.map_activated_on, 'U')
        return 0

    def get_user_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(country_id=obj.id, account_type=UserProfile.GOVERNMENT) \
            .difference(obj.users.all())
        return UserProfileSerializer(data, many=True).data

    def get_admin_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(country_id=obj.id, account_type=UserProfile.COUNTRY_ADMIN) \
            .difference(obj.admins.all())
        return UserProfileSerializer(data, many=True).data

    def get_super_admin_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(country_id=obj.id, account_type=UserProfile.SUPER_COUNTRY_ADMIN) \
            .difference(obj.super_admins.all())
        return UserProfileSerializer(data, many=True).data

    def get_country_questions(self, obj):
        request = self.context['request']

        if request.user and hasattr(request.user, 'userprofile') and can_read_private_questions(obj, request):
            queryset = CountryCustomQuestion.objects.filter(country_id=obj.id)
        else:
            queryset = CountryCustomQuestion.objects.filter(country_id=obj.id).exclude(private=True)

        return CountryCustomQuestionSerializer(queryset, many=True, read_only=True).data


class AdminCountrySerializer(SuperAdminCountrySerializer):
    class Meta(SuperAdminCountrySerializer.Meta):
        fields = COUNTRY_FIELDS + COUNTRY_ADMIN_FIELDS + ('users', 'admins', 'super_admins',)
        read_only_fields = READ_ONLY_COUNTRY_ADMIN_FIELDS + READ_ONLY_COUNTRY_FIELDS + COUNTRY_ADMIN_FIELDS \
            + ('super_admins',)


class CountrySerializer(SuperAdminCountrySerializer):
    class Meta(SuperAdminCountrySerializer.Meta):
        fields = COUNTRY_FIELDS
        read_only_fields = READ_ONLY_COUNTRY_FIELDS


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code', 'lat', 'lon', 'unicef_region')


DONOR_FIELDS = ("id", "name", "code", "logo", "logo_url", "cover", "cover_url", "cover_text", "footer_title",
                "footer_text", "partner_logos", "donor_questions")
READ_ONLY_DONOR_FIELDS = ("logo_url", "cover_url", "logo", "cover", "name", "code", "donor_questions")
DONOR_ADMIN_FIELDS = ('user_requests', 'admin_requests', 'super_admin_requests',)
READ_ONLY_DONOR_ADMIN_FIELDS = ("cover_text", "footer_title", "footer_text", "partner_logos",)


class SuperAdminDonorSerializer(UpdateAdminMixin, serializers.ModelSerializer):
    partner_logos = DonorPartnerLogoSerializer(many=True, read_only=True)
    donor_questions = serializers.SerializerMethodField()
    user_requests = serializers.SerializerMethodField()
    admin_requests = serializers.SerializerMethodField()
    super_admin_requests = serializers.SerializerMethodField()

    class Meta:
        model = Donor
        fields = DONOR_FIELDS + DONOR_ADMIN_FIELDS + ('users', 'admins', 'super_admins',)
        read_only_fields = READ_ONLY_DONOR_FIELDS + DONOR_ADMIN_FIELDS

    def get_user_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(donor_id=obj.id, account_type=UserProfile.DONOR) \
            .difference(obj.users.all())
        return UserProfileSerializer(data, many=True).data

    def get_admin_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(donor_id=obj.id, account_type=UserProfile.DONOR_ADMIN) \
            .difference(obj.admins.all())
        return UserProfileSerializer(data, many=True).data

    def get_super_admin_requests(self, obj):
        # figure out not yet assigned users
        data = UserProfile.objects.filter(donor_id=obj.id, account_type=UserProfile.SUPER_DONOR_ADMIN) \
            .difference(obj.super_admins.all())
        return UserProfileSerializer(data, many=True).data

    def get_donor_questions(self, obj):
        request = self.context['request']

        if request.user and hasattr(request.user, 'userprofile') and can_read_private_questions(obj, request):
            queryset = DonorCustomQuestion.objects.filter(donor_id=obj.id)
        else:
            queryset = DonorCustomQuestion.objects.filter(donor_id=obj.id).exclude(private=True)

        return DonorCustomQuestionSerializer(queryset, many=True, read_only=True).data


class AdminDonorSerializer(SuperAdminDonorSerializer):
    class Meta(SuperAdminDonorSerializer.Meta):
        fields = DONOR_FIELDS + DONOR_ADMIN_FIELDS + ('users', 'admins', 'super_admins',)
        read_only_fields = READ_ONLY_DONOR_ADMIN_FIELDS + READ_ONLY_DONOR_FIELDS + DONOR_ADMIN_FIELDS \
            + ('super_admins',)


class DonorSerializer(SuperAdminDonorSerializer):
    class Meta(SuperAdminDonorSerializer.Meta):
        fields = DONOR_FIELDS
        read_only_fields = READ_ONLY_DONOR_FIELDS


class DonorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('id', 'name', 'code')
