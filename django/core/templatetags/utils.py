from django import template
from django.contrib.sites.models import Site
from django.conf import settings

register = template.Library()


@register.simple_tag
def site_url():
    # return "https://{}".format(Site.objects.get_current().domain) # From Previous method, was grabbing the values from the django_site DB table
    return "https://{}".format(settings.SITE_URL)
