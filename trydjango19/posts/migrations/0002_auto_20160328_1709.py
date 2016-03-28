# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['timestamp', '-updated']},
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(upload_to='', blank=True, null=True),
        ),
    ]
