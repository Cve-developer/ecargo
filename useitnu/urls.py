from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('ecargo.urls')),
    path('admin/', admin.site.urls),
    path(('i18n/'), include('django.conf.urls.i18n')),
]
