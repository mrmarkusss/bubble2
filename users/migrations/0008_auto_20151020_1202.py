# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151012_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=40, verbose_name="\u0456\u043c'\u044f"),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=40, verbose_name='\u043f\u0440\u0456\u0437\u0432\u0438\u0449\u0435', blank=True),
        ),
    ]
