from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class WorkCategory(index.Indexed, models.Model):
    title = models.CharField(max_length=128)
    css_class = models.CharField(max_length=128)

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('css_class'),
    ]

    search_fields = [
        index.SearchField('title', partial_match=True),
    ]

    class Meta:
        verbose_name_plural = 'Work categories'

    def __str__(self):
        return self.title
