# Generated by Django 2.2.16 on 2021-02-08 10:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
