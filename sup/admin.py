from django.contrib import admin

from models import PublicationIdea


@admin.register(PublicationIdea)
class PublicationIdeaAdmin(admin.ModelAdmin):
    list_display = ['publication_title', 'full_name', 'affiliation']
    search_fields = ['publication_title',
                     'full_name', 'affiliation', 'keywords']
