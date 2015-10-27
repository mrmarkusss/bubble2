# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWallPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=4000, verbose_name='\u043a\u043e\u043d\u0442\u0435\u043d\u0442')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0434\u0430\u0442\u0430 \u0441\u0442\u0432\u043e\u0440\u0435\u043d\u043d\u044f', db_index=True)),
                ('author', models.ForeignKey(related_name='+', verbose_name='\u0430\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='wall_posts', verbose_name='\u0432\u043b\u0430\u043d\u0438\u043a \u0441\u0442\u0456\u043d\u0438', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
