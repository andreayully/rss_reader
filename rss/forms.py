from django import forms
from django.forms import ModelForm

from rss.models import RssFeedUser


class RssFeedUserForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = RssFeedUser
        exclude = ['user', 'subscribed', ]
        fields = ['title', 'feed_url', 'description', ]
