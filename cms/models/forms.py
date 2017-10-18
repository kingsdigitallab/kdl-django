import json

import os
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms.fields import FileField
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtaildocs.models import Document, get_document_model
from wagtail.wagtailforms.forms import FormBuilder
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField, FORM_FIELD_CHOICES
from wagtail.wagtailimages.fields import WagtailImageField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel


class FormField(AbstractFormField):
    FORM_FIELD_CHOICES = list(FORM_FIELD_CHOICES) + [('file', 'Upload PDF')]
    field_type = models.CharField(
        verbose_name=('field type'),
        max_length=16,
        choices=FORM_FIELD_CHOICES)
    page = ParentalKey('FormPage', related_name='form_fields')


# Extended to allow uploading of PDFs
class DocumentFormBuilder(FormBuilder):
    def create_document_upload_field(self, field, options):
        return FileField(**options)

    FIELD_TYPES = FormBuilder.FIELD_TYPES
    FIELD_TYPES.update({
        'file': create_document_upload_field,
    })


class FormPage(AbstractForm):
    form_builder = DocumentFormBuilder
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
    ]

    def filename_to_title(filename):
        from os.path import splitext
        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            # form = self.get_form(request.POST, page=self, user=request.user)  # Original line
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                return render(
                    request,
                    self.get_landing_page_template(request),
                    self.get_context(request)
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

    def process_form_submission(self, form):
        cleaned_data = form.cleaned_data

        for name, field in form.fields.iteritems():
            if isinstance(field, FileField):
                document_file_data = cleaned_data[name]
                if document_file_data:
                    DocumentModel = get_document_model()
                    doc = DocumentModel(
                        file=cleaned_data[name],
                        title=self.filename_to_title(cleaned_data[name].name),
                    )
                    doc.save()
                    cleaned_data.update({name: doc.id})
                else:
                    # remove the value from the data
                    del cleaned_data[name]

        form_data = json.dumps(cleaned_data, cls=DjangoJSONEncoder)
        submission_object = dict(
            page=self,
            form_data=form_data,
            user=form.user,
        )


# A refeactoring of WagtailImageField to create a field type for
# uploading files.

ALLOWED_EXTENSIONS = ['pdf']
SUPPORTED_FORMATS_TEXT = ("PDF")


class DocumentField(FileField):
    def __init__(self, *args, **kwargs):
        super(DocumentField, self).__init__(*args, **kwargs)

        # Get max upload size from settings
        self.max_upload_size = 10 * 1024 * 1024
        max_upload_size_text = filesizeformat(self.max_upload_size)

        # Help text
        if self.max_upload_size is not None:
            self.help_text = _(
                "Supported formats: %(supported_formats)s. Maximum filesize: %(max_upload_size)s."
            ) % {
                                 'supported_formats': SUPPORTED_FORMATS_TEXT,
                                 'max_upload_size': max_upload_size_text,
                             }
        else:
            self.help_text = _(
                "Supported formats: %(supported_formats)s."
            ) % {
                                 'supported_formats': SUPPORTED_FORMATS_TEXT,
                             }

        # Error messages
        self.error_messages['invalid_pdf'] = _(
            "Not a supported format. Supported formats: %s."
        ) % SUPPORTED_FORMATS_TEXT

        self.error_messages['invalid_pdf_known_format'] = _(
            "Not a valid %s PDF."
        )

        self.error_messages['file_too_large'] = _(
            "This file is too big (%%s). Maximum filesize %s."
        ) % max_upload_size_text

        self.error_messages['file_too_large_unknown_size'] = _(
            "This file is too big. Maximum filesize %s."
        ) % max_upload_size_text

    def check_image_file_format(self, f):
        # Check file extension
        extension = os.path.splitext(f.name)[1].lower()[1:]

        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(self.error_messages['invalid_pdf'], code='invalid_pdf')

        if hasattr(f, 'image'):
            # Django 1.8 annotates the file object with the PIL image
            image = f.image
        elif not f.closed:
            # Open image file
            file_position = f.tell()
            f.seek(0)

            try:
                image = Image.open(f)
            except IOError:
                # Uploaded file is not even an image file (or corrupted)
                raise ValidationError(self.error_messages['invalid_pdf_known_format'],
                                      code='invalid_pdf_known_format')

            f.seek(file_position)
        else:
            # Couldn't get the PIL image, skip checking the internal file format
            return

        image_format = extension.upper()
        if image_format == 'JPG':
            image_format = 'JPEG'

        internal_image_format = image.format.upper()
        if internal_image_format == 'MPO':
            internal_image_format = 'JPEG'

        # Check that the internal format matches the extension
        # It is possible to upload PSD files if their extension is set to jpg, png or gif. This should catch them out
        if internal_image_format != image_format:
            raise ValidationError(self.error_messages['invalid_pdf_known_format'] % (
                image_format,
            ), code='invalid_pdf_known_format')

    def check_image_file_size(self, f):
        # Upload size checking can be disabled by setting max upload size to None
        if self.max_upload_size is None:
            return

        # Check the filesize
        if f.size > self.max_upload_size:
            raise ValidationError(self.error_messages['file_too_large'] % (
                filesizeformat(f.size),
            ), code='file_too_large')

    def to_python(self, data):
        f = super(WagtailImageField, self).to_python(data)

        if f is not None:
            self.check_image_file_size(f)
            self.check_image_file_format(f)

        return f
