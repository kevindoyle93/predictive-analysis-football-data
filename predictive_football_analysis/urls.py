from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from football_data import urls as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
