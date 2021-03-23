from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy
from django.urls import reverse
import feedparser
from django.contrib.auth import authenticate, get_user_model
from rss.models import RssFeedUser
from rss.utils import get_feed_entries
import os


class RssFeedUserTest(TestCase):
    def setUp(self):
        self.rss_feed_user = mommy.make(RssFeedUser)
        rss_feed = self.rss_feed_user
        self.user = get_user_model().objects.create_user(username='test', email='test@example.com')
        user = self.user
        user.set_password('test123*')
        user.save()
        rss_feed.user = user
        rss_feed.feed_url = 'http://feeds.foxnews.com/foxnews/latest'
        rss_feed.save()

    def test_user_auth(self):
        rss_feed_user = self.rss_feed_user
        user = authenticate(username=rss_feed_user.user.username, password='test123*')
        self.assertTrue(isinstance(rss_feed_user.user, User))
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_feed_user_model(self):
        rss_feed_user = self.rss_feed_user
        self.assertTrue(isinstance(rss_feed_user, RssFeedUser))

    def test_view_uses_correct_template(self):
        self.client.login(username=self.user.username, password='test123*')
        resp = self.client.get(reverse('rss:rss-list'))
        self.assertTemplateUsed(resp, 'rss/rssfeeduser_list.html')

    def test_rss_create(self):
        self.client.login(username=self.user.username, password='test123*')
        resp = self.client.get(reverse('rss:create-rss'), {
            'title': 'fake news',
            'feed_url': 'http://rss.cnn.com/rss/edition.rss',
            'description': 'lorem ipsum',
            'user': self.user
        })
        self.assertEqual(resp.status_code, 200)

    def test_feedparser(self):
        rss_feed_user = self.rss_feed_user
        feed = feedparser.parse(rss_feed_user.feed_url)
        self.assertTrue('title' in feed.feed)
        self.assertTrue('link' in feed.feed)
        self.assertTrue('entries' in feed)

    def test_save_entries(self):
        response = get_feed_entries()
        log_path = "some path"
        self.assertEqual(response, "ALL ENTRIES WERE STORED")
        # self.assertTrue(os.path.exists(log_path))
