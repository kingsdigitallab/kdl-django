# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 09:52
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0039_wagtail_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='followup',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]
