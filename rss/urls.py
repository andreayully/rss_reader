from django.urls import path
from rss.views import RssFeedUserCreateView, RssFeedUserListView, FeddEntriesList, RssFeedUserUpdateView, \
    CancelSubscriptionRedirect

urlpatterns = [
    path('subscribe/', RssFeedUserCreateView.as_view(), name="create-rss"),
    path('subscribe/<str:pk>/', RssFeedUserUpdateView.as_view(), name="update-rss"),
    path('cancel-subscribe/<str:pk>/', CancelSubscriptionRedirect.as_view(), name="cancel-rss"),
    path('subscriptions/', RssFeedUserListView.as_view(), name="rss-list"),
    path('entries/<str:pk>/', FeddEntriesList.as_view(), name="feed-entries"),

]
