from __future__ import unicode_literals

from django import forms
from wagtail.wagtailcore.blocks import (
    CharBlock, FieldBlock, ListBlock, PageChooserBlock, RawHTMLBlock,
    RichTextBlock, StreamBlock, StructBlock, TextBlock, URLBlock
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


class PersonLinkBlock(StructBlock):
    # TODO At the moment Wagtail does not allow filtering by page type, but it
    # will in future versions. When it does this needs to be filtered by
    # PersonPage
    person = PageChooserBlock()
    description = RichTextBlock()


class PullQuoteStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('width-background', 'With background image'),
    ))


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()
    affiliation = CharBlock(required=False)
    style = PullQuoteStyleChoiceBlock()

    class Meta:
        template = 'cms/blocks/pullquote_block.html'


class BannerStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full-height', 'Full height'),
    ))


class BannerBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock()
    image = ImageChooserBlock(required=False)
    image_copyright = CharBlock(required=False)
    style = BannerStyleChoiceBlock()

    class Meta:
        template = 'cms/blocks/banner_block.html'


class OrderedListBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('title', CharBlock()),
        ('description', CharBlock())
    ]))

    class Meta:
        template = 'cms/blocks/ordered_list_block.html'


class ImageListBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('title', CharBlock()),
        ('subtitle', CharBlock()),
        ('description', CharBlock()),
        ('image', ImageChooserBlock())
    ]))

    class Meta:
        template = 'cms/blocks/image_list_block.html'


class ImageGridBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('image', ImageChooserBlock()),
        ('url', URLBlock(required=False)),
        ('page', PageChooserBlock(required=False))
    ], help_text='''
    Use either URL or page, if both are filled in URL takes precedence.'''))

    class Meta:
        template = 'cms/blocks/image_grid_block.html'


class CMSStreamBlock(StreamBlock):
    banner = BannerBlock(label='Banner section')
    ordered_list = OrderedListBlock(
        label='Ordered list section',
        help_text='Use this for sections similar to process')
    image_list = ImageListBlock(label='Image list section')
    image_grid = ImageGridBlock(label='Image grid section', icon='table')

    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    h5 = CharBlock(icon='title', classname='title')
    intro = RichTextBlock(icon='pilcrow')
    paragraph = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock(icon='openquote')

    image = ImageBlock(label='Aligned image', icon='image')
    document = DocumentChooserBlock(icon='doc-full-inverse')
    page = PageLinkBlock(icon='link')

    person = PersonLinkBlock(icon='user')
    organisation = OrganisationLinkBlock(icon='group')

    embed = EmbedBlock(icon='media')

    projects = ListBlock(PageChooserBlock(), label='Featured projects',
                         icon='pick')

    html = AlignedHTMLBlock(icon='code', label='Raw HTML')
