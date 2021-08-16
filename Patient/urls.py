from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('interface.urls', namespace='interface')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/', include('info.urls', namespace='info')),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
