from django.conf.urls import url, include
from django.contrib import admin

from football_data import urls as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
]
