from django.db import models
from django_countries.fields import CountryField
from wagtail.wagtailcore.models import Page


class PublicationIdea(models.Model):
    full_name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    Country = CountryField()
    email = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    publication_title = models.CharField(max_length=255)
    scholarly_discipline = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    summary = models.TextField(max_length=10000)
    link = models.URLField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)

