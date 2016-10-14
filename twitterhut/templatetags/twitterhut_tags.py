from datetime import datetime

from django import template
from django.template.defaultfilters import date
from django.utils.safestring import mark_safe
from twython import Twython

from ..views import get_user_timeline

register = template.Library()


@register.filter()
def tweet_date(value, arg=None):
    dt = datetime.strptime(value, '%a %b %d %H:%M:%S +0000 %Y')
    return date(dt, arg=arg)


@register.filter()
def tweet_to_html(tweet):
    return mark_safe(Twython.html_for_tweet(tweet))


@register.assignment_tag(takes_context=False)
def user_timeline(screen_name):
    return get_user_timeline(screen_name)
