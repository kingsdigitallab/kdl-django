# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 10:00
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0040_formpage_followup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formpage',
            old_name='followup',
            new_name='followup_text',
        ),
        migrations.AddField(
            model_name='formpage',
            name='subtitle',
            field=wagtail.wagtailcore.fields.RichTextField(default='Get in touch'),
        ),
    ]
