from django.db import models
from django_countries.fields import CountryField
from forms import PublicationIdeaForm
from django.shortcuts import render
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
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
    attachment = models.FileField(null=True,blank=True)



class PublicationIdeaPage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
            max_length=255, help_text="Title text to use for the 'thank you' page")
    thankyou_page_message = models.TextField(
        help_text="Text to use for the 'thank you' page")

    content_panels = Page.content_panels + [
                FieldPanel('intro', classname="full"),
                FieldPanel('thankyou_page_title'),
                FieldPanel('thankyou_page_message'),
            ]

    def serve(self, request):

        if request.method == 'POST':
            form = PublicationIdeaForm(request.POST)
            if form.is_valid():
                flavour = form.save()
                return render(request, 'sup/form_page_landing.html', {
                    'page': self,
                    'flavour': flavour,
                })
        else:
            form = PublicationIdeaForm()

        return render(request, 'sup/form_page.html', {
            'page': self,
            'form': form,
        })




    # class FlavourSuggestionPage(Page):
#         intro = RichTextField(blank=True)
#         thankyou_page_title = models.CharField(
#             max_length=255, help_text="Title text to use for the 'thank you' page")
#
#         # Note that there's nothing here for specifying the actual form fields -
#         # those are still defined in forms.py. There's no benefit to making these
#         # editable within the Wagtail admin, since you'd need to make changes to
#         # the code to make them work anyway.
#
#         content_panels = Page.content_panels + [
#             FieldPanel('intro', classname="full"),
#             FieldPanel('thankyou_page_title'),
#         ]
#
#         def serve(self, request):
#             from flavours.forms import FlavourSuggestionForm
#
#             if request.method == 'POST':
#                 form = FlavourSuggestionForm(request.POST)
#                 if form.is_valid():
#                     flavour = form.save()
#                     return render(request, 'flavours/thankyou.html', {
#                         'page': self,
#                         'flavour': flavour,
#                     })
#             else:
#                 form = FlavourSuggestionForm()
#
#             return render(request, 'flavours/suggest.html', {
#                 'page': self,
#                 'form': form,
#             })


# Template
# { % extends
# "base.html" %}
# { % load
# wagtailcore_tags %}
#
# { % block
# body_class %}template - suggest
# { % endblock %}
#
# { % block
# content %}
# < h1 > {{page.title}} < / h1 >
#
# {{page.intro | richtext}}
#
# < form
# action = "."
# method = "POST" >
# { % csrf_token %}
#
# {{form.as_p}}
#
# < p > < input
# type = "submit"
# value = "Suggest my flavour" > < / p >
# < / form >
# { % endblock %}