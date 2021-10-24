from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
