from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def site_url():
    return "https://{}".format(Site.objects.get_current().domain)
