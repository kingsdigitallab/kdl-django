# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 14:03


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_added_feed_image_to_blogpost_and_workpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='personpage',
            name='subtitle',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workpage',
            name='subtitle',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
