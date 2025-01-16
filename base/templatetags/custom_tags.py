from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag
def safe_url(url_name, *args, **kwargs):
    try:
        return reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return '#'
