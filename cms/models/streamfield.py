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
        ('default', 'Default'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()


class BannerStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('full-height', 'Full height'),
        ('home-banner full-height', 'Homepage'),
    ))


class BannerBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock()
    image = ImageChooserBlock(required=False)
    image_copyright = CharBlock(required=False)
    style = BannerStyleChoiceBlock()

    class Meta:
        template = 'cms/blocks/banner_block.html'


class FeaturedPageBlock(StructBlock):
    title = CharBlock(required=False)
    starred_page = PageChooserBlock()
    items = ListBlock(PageChooserBlock(), required=False)

    class Meta:
        template = 'cms/blocks/featured_page_block.html'


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'),
        ('mid', 'Mid width'), ('full-width', 'Full width'),
        ('hero', 'Hero'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

    class Meta:
        template = 'cms/blocks/image_block.html'


class ImageGridBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('image', ImageChooserBlock()),
        ('url', URLBlock(required=False)),
        ('page', PageChooserBlock(required=False))
    ]))

    class Meta:
        help_text = '''
        Use either URL or page, if both are filled in URL takes precedence.'''
        template = 'cms/blocks/image_grid_block.html'


class ImageListBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('title', CharBlock()),
        ('subtitle', CharBlock()),
        ('description', TextBlock()),
        ('image', ImageChooserBlock()),
        ('page', PageChooserBlock(required=False))
    ]))

    class Meta:
        template = 'cms/blocks/image_list_block.html'


class LinkStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('button', 'Button'),
    ))


class LinkBlock(StructBlock):
    url = URLBlock(required=False)
    page = PageChooserBlock(required=False)
    label = CharBlock()
    style = LinkStyleChoiceBlock()

    class Meta:
        help_text = '''
        Use either URL or page, if both are filled in URL takes precedence.'''
        template = 'cms/blocks/link_block.html'


class LiveFeedsBlock(StructBlock):
    blog_index_page = PageChooserBlock()
    twitter = CharBlock()

    class Meta:
        template = 'cms/blocks/live_feeds_block.html'


class OrderedListBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('title', CharBlock()),
        ('description', TextBlock())
    ]))
    label = CharBlock(required=False)
    page = PageChooserBlock(required=False)

    class Meta:
        template = 'cms/blocks/ordered_list_block.html'


class PullQuoteStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('with-background', 'With background image'),
    ))


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()
    affiliation = CharBlock(required=False)
    style = PullQuoteStyleChoiceBlock()

    class Meta:
        template = 'cms/blocks/pull_quote_block.html'


class UnorderedListBlock(StructBlock):
    title = CharBlock(required=False)
    items = ListBlock(StructBlock([
        ('title', CharBlock()),
        ('description', TextBlock()),
        ('page', PageChooserBlock(required=False))
    ]))
    label = CharBlock(required=False)
    page = PageChooserBlock(required=False)

    class Meta:
        template = 'cms/blocks/unordered_list_block.html'


class CMSStreamBlock(StreamBlock):
    banner = BannerBlock(label='Banner section')
    ordered_list = OrderedListBlock(
        label='Ordered list section',
        help_text='Use this for sections similar to process')
    unordered_list = UnorderedListBlock(
        label='Unordered list block section',
        help_text='Use this for sections similar to services')
    image_list = ImageListBlock(label='Image list section')
    image_grid = ImageGridBlock(label='Image grid section', icon='table')
    featured_pages = FeaturedPageBlock(
        label='Featured pages section', icon='doc-full')
    live_feeds = LiveFeedsBlock(
        label='Live feeds section (blog/twitter)', icon='wagtail')

    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    h5 = CharBlock(icon='title', classname='title')

    intro = RichTextBlock(icon='pilcrow')
    paragraph = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock(icon='openquote')

    image = ImageBlock(label='Aligned image', icon='image')
    document = DocumentChooserBlock(icon='doc-full-inverse')
    link = LinkBlock(icon='link')
    embed = EmbedBlock(icon='media')

    html = AlignedHTMLBlock(icon='code', label='Raw HTML')
