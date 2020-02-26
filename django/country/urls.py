from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from country.views import CountryViewSet, PartnerLogoViewSet, DonorViewSet, DonorPartnerLogoViewSet, \
    MapFileViewSet, CountryImageViewSet, DonorImageViewSet, CountryLandingPageViewSet, DonorLandingPageViewSet, \
    CountryCustomQuestionViewSet, DonorCustomQuestionViewSet, CountryLandingListPageViewSet, \
    DonorLandingListPageViewSet, CountryOfficeViewSet
from . import views

router = DefaultRouter()
router.register(r'landing-country', CountryLandingPageViewSet, base_name='landing-country'),
router.register(r'landing-country', CountryLandingListPageViewSet, base_name='landing-country'),
router.register(r'landing-donor', DonorLandingPageViewSet, base_name='landing-donor'),
router.register(r'landing-donor', DonorLandingListPageViewSet, base_name='landing-donor'),
router.register(r'countries', CountryViewSet, base_name='country')
router.register(r'countryoffices', CountryOfficeViewSet, base_name='countryoffice')
router.register(r'donors', DonorViewSet, base_name='donor')
router.register(r'country-partner-logos', PartnerLogoViewSet, base_name='country-partner-logo')
router.register(r'donor-partner-logos', DonorPartnerLogoViewSet, base_name='donor-partner-logo')
router.register(r'map-files', MapFileViewSet, base_name='map-file')
router.register(r'country-images', CountryImageViewSet, base_name='country-image')
router.register(r'donor-images', DonorImageViewSet, base_name='donor-image')
router.register(r'country-custom-questions', CountryCustomQuestionViewSet, base_name='country-custom-questions')
router.register(r'donor-custom-questions', DonorCustomQuestionViewSet, base_name='donor-custom-questions')

urlpatterns = [
                  url(r"^countries/map-download/(?P<country_id>\d+)/$",
                      view=views.MapDownloadViewSet.as_view({'get': 'map_download'}),
                      name="country-map-download"),
              ] + router.urls
