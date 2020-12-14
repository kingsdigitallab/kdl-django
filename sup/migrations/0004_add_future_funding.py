# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 14:06


import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sup', '0003_auto_20171110_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationidea',
            name='future_funding',
            field=models.TextField(default=b'', help_text=b'Please explain how this project has the potential to contribute to the possibility of obtaining external funding in the future and what external funding schemes you are considering, if any, to develop a fully-fledged product.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='publicationidea',
            name='attachment',
            field=models.FileField(blank=True, help_text=b'You can include 1 attachment (pdf format only; max size: 5MB) for example to visualise statically some aspects of your proposal.', null=True, upload_to=b'sup/', validators=[django.core.validators.FileExtensionValidator([b'pdf'])]),
        ),
        migrations.AlterField(
            model_name='publicationidea',
            name='link',
            field=models.URLField(blank=True, help_text=b'You can include a link to a website to provide further material to support your idea', null=True),
        ),
        migrations.AlterField(
            model_name='publicationidea',
            name='summary',
            field=models.TextField(help_text=b'Please provide a maximum 1000 words description of your publication idea. Make sure you explain where its innovative and experimental nature lie.', max_length=10000),
        ),
    ]
