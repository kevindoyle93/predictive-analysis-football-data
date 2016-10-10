from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from football_data import views

router = routers.DefaultRouter()
router.register(r'leagues', views.LeagueViewSet)
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
