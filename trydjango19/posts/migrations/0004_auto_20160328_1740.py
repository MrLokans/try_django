# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160328_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, blank=True, height_field='height_field', upload_to=posts.models.upload_location, width_field='width_field'),
        ),
    ]
