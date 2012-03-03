from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

import mixins

Language = mixins.Language


class Page(mixins.TranslatedMixin):
    '''Page object used to represent object's position inside a site objects
    hierarhy, activity state and can contains translation
    '''
    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')


class PageTranslation(mixins.ActivityMixin, mixins.HTMLMetaMixin,
                      mixins.NavigationMixin, mixins.TranslationMixin):
    '''Represent page translation for current language
    '''
    article = models.ForeignKey(Page, related_name='translations',
                                verbose_name=_('page'))
    content_type = models.ForeignKey(ContentType, null=True, blank=True,
                                     verbose_name=_('page content type'))

    class Meta:
        verbose_name = _('page translation')
        verbose_name_plural = _('pages translations')


class PageContent(models.Model):
    '''Base class represents page content for language. It's just a base class
    for all page content classes
    '''
    page = models.ForeignKey(PageTranslation, related_name='content')
    
    class Meta:
        abstract = True


class PageArticle(models.Model):
    '''Page contains an article
    '''
    text = models.TextField(_('page text'), help_text=_('page html content'))

    class Meta:
        verbose_name = _('page article')
        verbose_name_plural = _('page articles')
