# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from users.models import make_friends, break_friends


class NewsItemManager(models.Manager):
    def for_user(self, user):
        friends_ids = list(user.friends.values_list('pk', flat=True))
        friends_ids.append(user.pk)
        return self.filter(Q(user_id__in=friends_ids) | Q(target_id__in=friends_ids))


class NewsItem(models.Model):
    TYPE_WALL_POST = 'wall_post'
    TYPE_MAKE_FRIENDS = 'make_friends'
    TYPE_BREAK_FRIENDS = 'break_friends'
    TYPE_CHOICES = (
        (TYPE_WALL_POST, _(u'повідомлення на стіні')),
        (TYPE_MAKE_FRIENDS, _(u"створення дружніх зв'язків")),
        (TYPE_BREAK_FRIENDS, _(u"розрив дружніх зв'язків")),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    news_object = GenericForeignKey()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = NewsItemManager()

    class Meta:
        ordering = ('-created',)

    def get_template_for_display(self):
        return 'news/display_{}.html'.format(self.type)


@receiver(post_save, sender='users.UserWallPost')
def add_news_wall_post(sender, instance, created, **kwargs):
    if created:
        NewsItem.objects.create(
            user=instance.author,
            target=instance.user,
            type=NewsItem.TYPE_WALL_POST,
            news_object=instance
        )


@receiver(make_friends)
def add_news_make_friends(sender, user1_id, user2_id, **kwargs):
    NewsItem.objects.create(
        user_id=user1_id,
        target_id=user2_id,
        type=NewsItem.TYPE_MAKE_FRIENDS
    )


@receiver(break_friends)
def add_news_break_friends(sender, user1_id, user2_id, **kwargs):
    NewsItem.objects.create(
        user_id=user1_id,
        target_id=user2_id,
        type=NewsItem.TYPE_BREAK_FRIENDS
    )