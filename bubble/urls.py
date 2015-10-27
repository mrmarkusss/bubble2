from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language
from bubble import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^i18n/setlang/$', csrf_exempt(set_language), name='set_language'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('users.urls')),
    url(r'', include('auths.urls')),
    url(r'', include('dialogs.urls')),
    url(r'', include('news.urls')),

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend([
    url(r'', include('django.contrib.flatpages.urls'))
])
