from django.contrib import admin
from .actions import export_to_csv
from .models import PublicationIdea


@admin.register(PublicationIdea)
class PublicationIdeaAdmin(admin.ModelAdmin):
    export_filename = 'sup_export'
    list_display = ['publication_title', 'full_name', 'affiliation',
                    'country', 'email', 'website', 'publication_title',
                    'scholarly_discipline', 'keywords', 'summary', 'link',
                    'attachment', 'future_funding'
                    ]
    actions = [export_to_csv]
    search_fields = ['publication_title',
                     'full_name', 'affiliation', 'keywords']
