from rss.models import RssFeedUser, FeedEntries
from datetime import datetime, timedelta
from django.utils import timezone
import os
import time
import feedparser


def log_entries_file(feed_obj):
    filename = "log_entries.txt"
    if os.path.exists(filename):
        action = 'a'
    else:
        action = 'w'
    log_file = open(filename, action)
    log_file.write(f'Feed {feed_obj.title} updated at {timezone.localtime(timezone.now())}. '
                   f'{feed_obj.feedentries_set.count()} entries \n')
    log_file.close()


def save_entries(feed_obj):
    """save entries from a feed"""
    feed = feedparser.parse(feed_obj.feed_url)
    for i in range(len(feed.entries)):
        external_id = feed.entries[i].id if 'id' in feed.entries[i] else feed.entries[i].link
        description = feed.entries[i].description if 'description' in feed.entries[i] else None
        published = None
        if 'published_parsed' in feed.entries[i]:
            my_time = feed.entries[i].published_parsed
            timestamp = time.mktime(my_time)
            my_datetime = datetime.fromtimestamp(timestamp)
            published = my_datetime - timedelta(hours=5)
        FeedEntries.objects.create(
            feed=feed_obj,
            title=feed.entries[i].title,
            description=description,
            link=feed.entries[i].link,
            published=published,
            external_id=external_id)


def get_feed_entries():
    rss = RssFeedUser.objects.filter(subscribed=True)
    for feed_obj in rss:
        FeedEntries.objects.filter(feed=feed_obj).delete()
        save_entries(feed_obj)
        feed_obj.last_update = timezone.now()
        feed_obj.save()
        log_entries_file(feed_obj)
    return "ALL ENTRIES WERE STORED"


def save_new_rss_subscription(feed_pk):
    feed_obj = RssFeedUser.objects.get(id=feed_pk)
    save_entries(feed_obj)
    feed_obj.last_update = timezone.now()
    feed_obj.save()
    log_entries_file(feed_obj)
