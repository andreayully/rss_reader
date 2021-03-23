from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class RssFeedUser(models.Model):
    """
    Model for user and RSS Feed
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    feed_url = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200)
    subscribed = models.BooleanField(default=True)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class FeedEntries(models.Model):
    """
    Model for entries
    """
    feed = models.ForeignKey(RssFeedUser, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=2048)
    published = models.DateTimeField(blank=True, null=True)
    external_id = models.CharField(max_length=2048, unique=True)

    def __str__(self):
        return self.feed.title
