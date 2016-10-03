from __future__ import unicode_literals

from django import forms
from wagtail.wagtailcore.blocks import (
    BooleanBlock, CharBlock, FieldBlock, ListBlock, PageChooserBlock,
    RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock
)
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = 'code'


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'),
        ('mid', 'Mid width'), ('full', 'Full width'),
        ('hero', 'Hero'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class OrganisationLinkBlock(StructBlock):
    # TODO At the moment Wagtail does not allow filtering by page type, but it
    # will in future versions. When it does this needs to be filtered by
    # PersonPage
    organisation = PageChooserBlock()
    description = RichTextBlock()


class PageLinkBlock(StructBlock):
    page = PageChooserBlock()
    label = CharBlock()

    class Meta:
        icon = 'link'


class PersonLinkBlock(StructBlock):
    # TODO At the moment Wagtail does not allow filtering by page type, but it
    # will in future versions. When it does this needs to be filtered by
    # PersonPage
    person = PageChooserBlock()
    description = RichTextBlock()


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


class CMSStreamBlock(StreamBlock):
    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    h5 = CharBlock(icon='title', classname='title')
    intro = RichTextBlock(icon='pilcrow')
    paragraph = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock()

    image = ImageBlock(label='Aligned image', icon='image')
    document = DocumentChooserBlock(icon='doc-full-inverse')
    page = PageLinkBlock(icon='link')

    person = PersonLinkBlock(icon='user')
    organisation = OrganisationLinkBlock(icon='group')

    embed = EmbedBlock(icon='media')

    projects = ListBlock(PageChooserBlock(), label='Featured projects',
                         icon='pick')
    latest_blog_posts = BooleanBlock(
        required=True, label='Show latest blog posts', icon='date')
    twitter = CharBlock(icon='wagtail')

    html = AlignedHTMLBlock(icon='code', label='Raw HTML')
    map_html = AlignedHTMLBlock(icon='code', label='Map HTML')
