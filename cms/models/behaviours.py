
from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailcore.fields import StreamField

from .streamfield import CMSStreamBlock


class WithStreamField(models.Model):
    body = StreamField(CMSStreamBlock())

    class Meta:
        abstract = True
