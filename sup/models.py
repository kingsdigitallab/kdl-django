import django.forms as forms
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat
from django_countries.fields import CountryField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from django.conf import settings
from django.core.validators import FileExtensionValidator
from captcha.fields import CaptchaField


class PublicationIdea(models.Model):

    full_name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    country = CountryField()
    email = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    publication_title = models.CharField(max_length=255)
    scholarly_discipline = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    summary = models.TextField(max_length=10000)
    link = models.URLField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True,
                                  upload_to=settings.SUP_URL,
                                  validators=[FileExtensionValidator(['pdf'])])


class PublicationIdeaForm(forms.ModelForm):
    captcha = CaptchaField()
    max_upload_size = 10 * 1024 * 1024
    # Guidance called for max words not characters but could change
    summary_max_words = 1000

    def filename_to_title(filename):
        from os.path import splitext
        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()

    def check_image_file_size(self, f):
        # Upload size checking can be disabled by setting max upload size to
        # None
        if self.max_upload_size is None:
            return

        # Check the filesize
        if f.size > self.max_upload_size:
            raise ValidationError(self.error_messages['file_too_large'] % (
                filesizeformat(f.size),
            ), code='file_too_large')

    def clean_summary(self):
        summary = self.cleaned_data.get("summary", False)
        if self.summary_max_words is None:
            return summary
        elif len(summary.split()) > self.summary_max_words:
            raise ValidationError(
                "Summary is {} words long.  Maximum is 1000".format(
                    len(summary.split())))
        return summary

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment", None)
        if attachment:
            self.check_image_file_size(attachment)

        return attachment

    class Meta:
        model = PublicationIdea
        exclude = []


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
            form = PublicationIdeaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return render(request, 'sup/form_page_landing.html', {
                    'page': self,
                })
        else:
            form = PublicationIdeaForm()

        return render(request, 'sup/form_page.html', {
            'page': self,
            'form': form,
        })
