import logging

from django.conf import settings
from django.core.cache import cache
from twython import Twython, TwythonAuthError, TwythonError

logger = logging.getLogger(__name__)


def get_user_timeline(screen_name):
    timeline = cache.get('twitter_timeline')

    if not timeline:
        try:
            twitter = authenticate()

            timeline = twitter.get_user_timeline(
                screen_name=screen_name,
                count=settings.TWITTER_USER_TIMELINE_ITEMS)

            cache.set('twitter_timeline', timeline,
                      settings.TWITTER_CACHE_TIMEOUT)
        except TwythonError as e:
            logger.error(e)
            raise e

    return timeline


def authenticate():
    twitter = cache.get('twitter')

    if not twitter:
        try:
            twitter = Twython(settings.TWITTER_API_KEY,
                              settings.TWITTER_API_SECRET,
                              settings.TWITTER_ACCESS_TOKEN,
                              settings.TWITTER_ACCESS_TOKEN_SECRET)

            cache.set('twitter', twitter, settings.TWITTER_CACHE_TIMEOUT)
        except TwythonAuthError as e:
            logger.error(e)
            raise e

    return twitter
