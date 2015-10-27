from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/(?P<user_id>\d+)/$', views.UserProfileView.as_view(), name='user_profile'),
    url(r'^settings/$', views.UserSettings.as_view(), name='settings'),
    url(r'^friends/$', views.UserFriendsView.as_view(), name='friends'),
    url(r'^search/$', views.UserSearchPeople.as_view(), name='search'),
    url(r'^friends/incoming$', views.UserFriendsIncomeView.as_view(), name='friends_income'),
    url(r'^friends/outcoming$', views.UserFriendsOutcomeView.as_view(), name='friends_outcome'),

    url(r'^api/friendship', views.FriendshipAPIView.as_view(), name='user_friendship_api'),
]