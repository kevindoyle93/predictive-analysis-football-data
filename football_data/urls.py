from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from football_data import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^leagues/$',
        views.LeagueList.as_view(),
        name='league-list'),
    url(r'^leagues/(?P<pk>[0-9]+)/$',
        views.LeagueDetail.as_view(),
        name='league-detail'),
    url(r'^teams/$',
        views.TeamList.as_view(),
        name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$',
        views.TeamDetail.as_view(),
        name='team-detail'),
    url(r'^teams/(?P<pk>[0-9]+)/matches/$',
        views.TeamMatchesList.as_view(),
        name='team-matches'),
    url(r'^matches/$',
        views.MatchList.as_view(),
        name='match-list'),
    url(r'^matches/(?P<pk>[0-9]+)/$',
        views.MatchDetail.as_view(),
        name='match-detail'),
    url(r'get_tactical_advice/$',
        views.generate_prediction,
        name='get-tactical-advice'),
    url(r'coaches/$',
        views.CoachCreate.as_view(),
        name='coaches-create'),
    url(r'^coaches/matches/$',
        views.AppMatchList.as_view(),
        name='app-matches'),
]
