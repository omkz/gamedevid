from django.conf.urls.defaults import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('home.urls', namespace='home')),   
    url(r'^users/', include('users.urls', namespace='users')),   
    url(r'^posts/', include('posts.urls', namespace='posts')),   
    url(r'^tags/', include('tags.urls', namespace='tags')),   
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
