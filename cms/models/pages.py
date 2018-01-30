from __future__ import unicode_literals

import logging

from captcha.fields import CaptchaField
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, FieldRowPanel,
                                                InlinePanel, MultiFieldPanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from wagtail.wagtailforms.forms import FormBuilder
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from .behaviours import WithContactFields, WithFeedImage, WithStreamField
from .snippets import WorkCategory

logger = logging.getLogger(__name__)


def _paginate(request, items):
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        items = paginator.page(1)

    return items


class HomePage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = [
        'BlogIndexPage', 'FormPage', 'IndexPage', 'OrganisationIndexPage',
        'PersonIndexPage', 'RichTextPage', 'WorkIndexPage',
        'sup.PublicationIdeaPage'
    ]


HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

HomePage.promote_panels = Page.promote_panels


class IndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = [
        'FormPage', 'IndexPage', 'RichTextPage', 'sup.PublicationIdeaPage'
    ]


IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

IndexPage.promote_panels = Page.promote_panels


class RichTextPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = []


RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

RichTextPage.promote_panels = Page.promote_panels


class PersonIndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['PersonPage']


PersonIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

PersonIndexPage.promote_panels = Page.promote_panels


class PersonPage(Page, WithContactFields, WithFeedImage, WithStreamField):
    subtitle = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    intro = RichTextField(blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    subpage_types = []


PersonPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('subtitle', classname='full title'),
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('intro', classname='full'),
    StreamFieldPanel('body'),
    MultiFieldPanel(WithContactFields.panels, 'Contact information'),
]

PersonPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class OrganisationIndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['OrganisationPage']


OrganisationIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

OrganisationIndexPage.promote_panels = Page.promote_panels


class OrganisationPage(Page, WithContactFields, WithFeedImage,
                       WithStreamField):
    intro = RichTextField(blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    subpage_types = []


OrganisationPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    StreamFieldPanel('body'),
    MultiFieldPanel(WithContactFields.panels, 'Contact information'),
]

OrganisationPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class WorkIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['WorkPage']

    @property
    def works(self):
        works = WorkPage.objects.live().descendant_of(self)

        return works

    @route(r'^$')
    def all_works(self, request):
        works = self.works

        return render(request, self.get_template(request),
                      {'self': self, 'works': _paginate(request, works)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_works(request)

        works = self.works.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'works': _paginate(request, works),
                'filter_type': 'tag', 'filter': tag
            }
        )


WorkIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

WorkIndexPage.promote_panels = Page.promote_panels


class WorkPageTag(TaggedItemBase):
    content_object = ParentalKey('WorkPage', related_name='tagged_items')


class WorkPage(Page, WithStreamField, WithFeedImage):
    subtitle = models.CharField(max_length=256)
    category = models.ForeignKey(WorkCategory, blank=True, null=True,
                                 on_delete=models.SET_NULL,)
    tags = ClusterTaggableManager(through=WorkPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('subtitle'),
        index.SearchField('category'),
        index.RelatedFields('tags', [
                            index.SearchField('name'),
                            ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a blog index
        return WorkIndexPage.objects.ancestor_of(self).last()


WorkPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('subtitle', classname='full title'),
    SnippetChooserPanel('category'),
    StreamFieldPanel('body'),
]

WorkPage.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
    ImageChooserPanel('feed_image'),
]


class BlogIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        posts = BlogPost.objects.live().descendant_of(self)

        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )


BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

BlogIndexPage.promote_panels = Page.promote_panels


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items')


class BlogPost(Page, WithStreamField, WithFeedImage):
    date = models.DateField()
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date'),
        index.RelatedFields('tags', [
                            index.SearchField('name'),
                            index.SearchField('slug'),
                            ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a blog index
        return BlogIndexPage.objects.ancestor_of(self).last()


BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
]

BlogPost.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
    ImageChooserPanel('feed_image'),
]


class CaptchaFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = 'captcha'

    def __init__(self, fields):
        super(CaptchaFormBuilder, self).__init__(fields)

        self.FIELD_TYPES.update(
            {self.CAPTCHA_FIELD_NAME: self.create_captcha_field})

    def create_captcha_field(self, field, options):
        return CaptchaField(**options)

    @property
    def formfields(self):
        fields = super(CaptchaFormBuilder, self).formfields
        fields[self.CAPTCHA_FIELD_NAME] = CaptchaField(required=True)

        return fields


class FormField(AbstractFormField):
    page = ParentalKey('FormPage',
                       on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    form_builder = CaptchaFormBuilder
