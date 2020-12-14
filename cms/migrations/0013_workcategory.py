# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 14:40


from django.db import migrations, models
import wagtail.wagtailsearch.index


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_added_subtitle_to_personpage_and_workpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('css_class', models.CharField(max_length=128)),
            ],
            bases=(wagtail.wagtailsearch.index.Indexed, models.Model),
        ),
    ]
