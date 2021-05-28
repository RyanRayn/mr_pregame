
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('games/', include('games.urls')),
    path('management/', include('management.urls')),
    path('matchups/', include('matchups.urls')),
    path('profile/', include('profiles.urls')),
    url(r'^$', views.handler404),
    url(r'^$', views.handler500),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'mr_pregame.views.handler404'
handler500 = 'mr_pregame.views.handler500'
