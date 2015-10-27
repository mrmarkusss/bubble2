from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_avatar(user):
    try:
        return user.avatar.url
    except ValueError:
        return '{}users/img/default.png'.format(settings.STATIC_URL)