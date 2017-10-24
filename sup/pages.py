from django.shortcuts import render
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from django.db import models
from forms import PublicationIdeaForm


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