# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 13:13


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sup', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicationidea',
            old_name='Country',
            new_name='country',
        ),
    ]
