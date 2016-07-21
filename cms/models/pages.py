from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from .behaviours import WithContactFields, WithFeedImage, WithStreamField


class HomePage(Page, WithStreamField):
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = ['IndexPage', 'PersonIndexPage', 'RichTextPage']

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

HomePage.promote_panels = Page.promote_panels


class IndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = ['IndexPage', 'RichTextPage']


IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

IndexPage.promote_panels = Page.promote_panels


class RichTextPage(Page, WithStreamField):
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = []

RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

RichTextPage.promote_panels = Page.promote_panels


class PersonIndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    subpage_types = ['PersonPage']

PersonIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

PersonIndexPage.promote_panels = Page.promote_panels


class PersonPage(Page, WithContactFields, WithFeedImage, WithStreamField):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    intro = RichTextField(blank=True)
    search_fields = Page.search_fields + (
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('body'),
    )

    subpage_types = []

PersonPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('intro', classname='full'),
    MultiFieldPanel(WithContactFields.panels, 'Contact'),
    StreamFieldPanel('body'),
]

PersonPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
