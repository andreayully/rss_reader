from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, RedirectView
from django.urls import reverse_lazy
from rss.forms import RssFeedUserForm
from rss.models import RssFeedUser, FeedEntries
from rss.tasks import save_new_rss_subscription_task


class RssFeedUserCreateView(LoginRequiredMixin, CreateView):
    """
    View for creation User and RSS Feed relation
    """
    model = RssFeedUser
    form_class = RssFeedUserForm
    template_name = 'rss/rss_subscription.html'
    success_url = reverse_lazy('rss:rss-list')

    def form_valid(self, form):
        rss = form.save(commit=False)
        rss.user = self.request.user
        form.save()
        save_new_rss_subscription_task.delay(form.instance.pk)
        return super(RssFeedUserCreateView, self).form_valid(form)


class RssFeedUserUpdateView(LoginRequiredMixin, UpdateView):
    model = RssFeedUser
    form_class = RssFeedUserForm
    template_name = 'rss/rss_subscription.html'

    def get_success_url(self):
        feed_pk = self.kwargs['pk']
        return reverse_lazy('rss:feed-entries', kwargs={'pk': feed_pk})


class RssFeedUserListView(LoginRequiredMixin, ListView):
    """
    View for list user subcription
    """
    model = RssFeedUser

    def get_queryset(self):
        return RssFeedUser.objects.filter(user=self.request.user, subscribed=True)

    def get_context_data(self, **kwargs):
        context = super(RssFeedUserListView, self).get_context_data(**kwargs)
        context['unsubscribe'] = RssFeedUser.objects.filter(user=self.request.user, subscribed=False)
        return context


class FeddEntriesList(LoginRequiredMixin, TemplateView):
    """
    List for entries in a Feed
    """
    template_name = 'rss/feed_entries.html'

    def get_context_data(self, **kwargs):
        context = super(FeddEntriesList, self).get_context_data(**kwargs)
        user = self.request.user
        rss_feed = RssFeedUser.objects.get(id=self.kwargs['pk'])
        entries = FeedEntries.objects.filter(feed=rss_feed.id)
        context['user'] = user
        context['rss_feed'] = rss_feed
        context['entries'] = entries
        return context


class CancelSubscriptionRedirect(LoginRequiredMixin, RedirectView):
    is_permanent = True
    url = reverse_lazy('rss:rss-list')

    def dispatch(self, request, *args, **kwargs):
        self.cancel_rss_subscription()
        return super(CancelSubscriptionRedirect, self).dispatch(request, *args, **kwargs)

    def cancel_rss_subscription(self):
        """
        Cancel RSS Subscription
        """
        rss = RssFeedUser.objects.get(id=self.kwargs["pk"])
        rss.subscribed = False if rss.subscribed else True
        rss.save()
