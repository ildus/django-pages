from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityMixin(object):
    '''Mixin contains active field
    '''
    active = models.BooleanField(verbose_name=_('Is active'), default=True)


class HTMLMetaMixin(object):
    '''Mixin contains fields can be used to generate html meta tags and some
    other html > head tags

        title - <title> tag
        meta_description - <meta name="description" content="..." />
        meta_keywords - <meta name="keywords" content="..." />
    '''
    title = models.CharField(max_length=255, verbose_name=_('Title'),
                             blank=True, help_text=_('The title tag'))
    meta_description = models.TextField(verbose_name=_('Description'),
                             blank=True, help_text=_('Tag meta description'))
    meta_keywords = models.TextField(verbose_name=_('Keywords'), blank=True,
                                     help_text=_('Tag meta keywords'))


class Language(models.Model):
    '''Model represents language
    '''


class NavigationMixin(object):
    '''
    '''
    alias = models.SlugField(verbose_name=_('Alias'), unique=False,
                             help_text=_('URL string alias (slug)'))
    header = models.CharField(max_length=255, verbose_name=_('Header'),
                              blank=True, help_text=_('H1 page tag'))
