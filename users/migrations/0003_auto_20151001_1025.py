# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmed_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmed_registration',
            field=models.BooleanField(default=True, verbose_name='confirmed registration'),
        ),
    ]
