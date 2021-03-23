from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from rss.utils import get_feed_entries, save_new_rss_subscription
from rss_reader.celery import app

logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'get-feed-entries': {
        'task': 'rss.tasks.get_feed_entries_task',
        'schedule': crontab(hour='*/12')
    },

}

app.conf.timezone = 'UTC'


@shared_task
def get_feed_entries_task():
    """
    Saves entries for feed
    """
    get_feed_entries()
    logger.info("Entries for Feed")


@shared_task
def save_new_rss_subscription_task(feed_obj):
    """
    Task to save entries for a new feed subscription
    """
    save_new_rss_subscription(feed_obj)
    logger.info("Entries for new Feed subcription")
