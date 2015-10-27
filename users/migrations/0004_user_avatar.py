# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151001_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=users.models.get_image_file_name, verbose_name='\u0430\u0432\u0430\u0442\u0430\u0440\u043a\u0430', blank=True),
        ),
    ]
