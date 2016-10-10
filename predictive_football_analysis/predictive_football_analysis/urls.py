from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from football_data import views

router = routers.DefaultRouter()
router.register(r'league', views.LeagueViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'stadium', views.StadiumViewSet)
router.register(r'player', views.PlayerViewSet)
router.register(r'match', views.MatchViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
