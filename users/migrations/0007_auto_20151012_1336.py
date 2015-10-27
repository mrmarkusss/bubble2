# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_user', models.ForeignKey(related_name='out_friend_invites', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='in_friend_invites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='friendinvite',
            unique_together=set([('from_user', 'to_user')]),
        ),
    ]
