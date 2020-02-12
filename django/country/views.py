import pycountry
import requests

from requests import RequestException
from django.conf import settings
from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from user.models import UserProfile
from .permissions import InAdminOrReadOnly, InSuperAdmin, InCountryAdminOrReadOnly, \
    InCountrySuperAdmin, InDonorSuperAdmin
from .models import Country, Donor, PartnerLogo, DonorPartnerLogo, MapFile, \
    CountryCustomQuestion, DonorCustomQuestion
from .serializers import CountrySerializer, SuperAdminCountrySerializer, AdminCountrySerializer, \
    PartnerLogoSerializer, DonorSerializer, SuperAdminDonorSerializer, AdminDonorSerializer, \
    DonorPartnerLogoSerializer, MapFileSerializer, CountryImageSerializer, DonorImageSerializer, \
    DonorCustomQuestionSerializer, CountryCustomQuestionSerializer, CountryListSerializer, DonorListSerializer


class CountryLandingPageViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryLandingListPageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.only('id', 'name', 'code')
    serializer_class = CountryListSerializer


class DonorLandingPageViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class DonorLandingListPageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Donor.objects.only('id', 'name', 'code')
    serializer_class = DonorListSerializer


class AdminPermissionMixin:
    permission_classes = (IsAuthenticated, InAdminOrReadOnly,)


class SuperAdminPermissionMixin:
    permission_classes = (IsAuthenticated, InSuperAdmin,)


class CountryAdminPermissionMixin:
    permission_classes = (IsAuthenticated, InCountryAdminOrReadOnly,)


class CountrySuperAdminPermissionMixin:
    permission_classes = (IsAuthenticated, InCountrySuperAdmin,)


class DonorSuperAdminPermissionMixin:
    permission_classes = (IsAuthenticated, InDonorSuperAdmin,)


class CountryViewSet(AdminPermissionMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_serializer_class(self):
        if self.request and self.action in ['update', 'retrieve', 'partial_update'] \
                and self.request.user.is_authenticated:
            country = self.get_object()
            profile = self.request.user.userprofile
            if profile.account_type == UserProfile.COUNTRY_ADMIN and profile in country.admins.all():
                return AdminCountrySerializer
            if profile.account_type == UserProfile.SUPER_COUNTRY_ADMIN and profile in country.super_admins.all() \
                    or self.request.user.is_superuser:
                return SuperAdminCountrySerializer
        return super().get_serializer_class()


class DonorViewSet(AdminPermissionMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

    def get_serializer_class(self):
        if self.request and self.action in ['update', 'retrieve', 'partial_update'] \
                and self.request.user.is_authenticated:
            donor = self.get_object()
            profile = self.request.user.userprofile
            if profile.account_type == UserProfile.DONOR_ADMIN and profile in donor.admins.all():
                return AdminDonorSerializer
            if profile.account_type == UserProfile.SUPER_DONOR_ADMIN and profile in donor.super_admins.all() \
                    or self.request.user.is_superuser:
                return SuperAdminDonorSerializer
        return super().get_serializer_class()


class PartnerLogoViewSet(CountrySuperAdminPermissionMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PartnerLogo.objects.all()
    serializer_class = PartnerLogoSerializer
    parser_classes = (MultiPartParser, FormParser)


class DonorPartnerLogoViewSet(DonorSuperAdminPermissionMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = DonorPartnerLogo.objects.all()
    serializer_class = DonorPartnerLogoSerializer
    parser_classes = (MultiPartParser, FormParser)


class MapFileViewSet(CountryAdminPermissionMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MapFile.objects.all()
    serializer_class = MapFileSerializer
    parser_classes = (MultiPartParser, FormParser)


class MapDownloadViewSet(viewsets.ViewSet):
    @staticmethod
    def map_download(request, country_id):
        obj = get_object_or_404(Country.objects.all(), id=country_id)
        country = pycountry.countries.get(alpha_2=obj.code)
        url = ("https://wambachers-osm.website/boundaries/exportBoundaries?"
               "cliVersion=1.0&cliKey={}&exportFormat=json&exportLayout=single"
               "&exportAreas=land&union=false&from_AL=2&to_AL=6&selected={}").format(
            settings.OSM_MAP_CLI_KEY, country.alpha_3)

        osm_request = requests.get(url, stream=True)
        try:
            osm_request.raise_for_status()
        except RequestException:
            return HttpResponse(status=osm_request.status_code, content='Download failed', content_type='text/plain')
        else:
            response = HttpResponse(osm_request.content, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format('exportBoundaries.zip')
            return response


class CountryImageViewSet(SuperAdminPermissionMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountryImageSerializer
    parser_classes = (MultiPartParser, FormParser)


class DonorImageViewSet(SuperAdminPermissionMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorImageSerializer
    parser_classes = (MultiPartParser, FormParser)


class SetOrderToMixin:
    @action(methods=['post'], detail=True)
    def set_order_to(self, request, pk=None):
        custom_question = self.get_object()
        to_id = request.data.get('to')

        if to_id is not None:
            try:
                custom_question.to(int(to_id))
                return Response(custom_question.get_order())
            except (ValueError, TypeError):
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CountryCustomQuestionViewSet(SetOrderToMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CountryCustomQuestion.objects.all()
    serializer_class = CountryCustomQuestionSerializer


class DonorCustomQuestionViewSet(SetOrderToMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = DonorCustomQuestion.objects.all()
    serializer_class = DonorCustomQuestionSerializer
