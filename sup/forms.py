import django.forms as forms
import magic
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from sup.models import PublicationIdea


class PublicationIdeaForm(forms.ModelForm):
    allowed_attachment_types = ['PDF', ]
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
        file = self.cleaned_data.get("file", False)
        with magic.Magic() as m:
            filetype = m.from_buffer(file.read())
            if filetype not in self.allowed_attachment_types:
                raise ValidationError(
                    "File {} is not a valid attachment type.".format(filetype))
        self.check_image_file_size(file)
        return file

    class Meta:
        model = PublicationIdea
        exclude = []
