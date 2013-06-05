'''Url mapping for pages
'''
from django.conf.urls.defaults import patterns, url
from . import views
from django.conf import settings


if settings.APPEND_SLASH:
    reg = url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/$', views.page_view, name='show_page')
else:
    reg = url(r'^(?P<slug>[0-9A-Za-z-_.//]+)$', views.page_view, name='show_page')

urlpatterns = patterns('',
    reg,
    url('^$', views.page_view, name='show_page'),
)
