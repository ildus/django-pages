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


class Layout(mixins.ActivityMixin):
    '''Layout for building pages
    '''
    name = models.CharField(_('layout name'), max_length=128)
    template = models.CharField(_('layout template'), max_length=256)
    is_default = models.BooleanField(_('is default placeholde'), default=False)

    class Meta:
        verbose_name = _('page layout')
        verbose_name_plural = _('page layouts')

    def save(self, *args, **kwargs):
        '''Save layout
        Because it can be only one layout selected update all other layouts to
        set their is_default values to False if current layout's is_default
        was set to True
        '''
        if self.is_default:
            query = self.__class__.objects.all()
            if self.pk:
                query = query.exclude(pk=self.pk)
            query = query.update(is_default=False)
        return super(Layout, self).save(*args, **kwargs)


class Placeholder(models.Model):
    '''Placeholder in template
    '''
    alias = models.CharField(_('access name'), max_length=64, primary_key=True,
                             help_text=_('name for accessing from templates'))
    name = models.CharField(_('verbose name'), max_length=256,
                            help_text=_('name shown in admin interface'))

    def save(self, *args, **kwargs):
        '''Save placeholder into database
        If there is no name set take it from alias
        '''
        if not self.name:
            self.name = self.alias
        return super(Placeholder, self).save(*args, **kwargs)


class PageTranslation(mixins.ActivityMixin, mixins.HTMLMetaMixin,
                      mixins.NavigationMixin, mixins.TranslationMixin):
    '''Represent page translation for current language
    '''
    page = models.ForeignKey(Page, related_name='translations',
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
