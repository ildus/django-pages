from django.db import models
from django.utils.translation import get_language_info, ugettext_lazy as _


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
    code = models.CharField(_('Language code'), max_length=5, primary_key=True)

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')

    def __str__(self):
        '''Get language name for it's code
        '''
        return get_language_info(self.code)['name']

    def __unicode__(self):
        '''Get language name for it's code
        '''
        return self.__str__()

    def __repr__(self):
        '''Represent
        '''
        return ''.join(('<', self.__class__.__name__, ': "', self.code, '">'))


class NavigationMixin(object):
    '''
    '''
    alias = models.SlugField(verbose_name=_('Alias'), unique=False,
                             help_text=_('URL string alias (slug)'))
    header = models.CharField(max_length=255, verbose_name=_('Header'),
                              blank=True, help_text=_('H1 page tag'))


class TranslatedMixin(object):
    '''Mixin adds method to select object translation for specified language
    from translations_set field (required to be set). Can be used to make
    objects translated to different languages.

    As example for classes:

        class Article(models.Model, TranslatedMixin):
            name = models.CharField(max_length=255)

        class ArticleTranslation(TranslationMixin, models.Model):
            title = models.CharField(max_length=255)
            content = models.TextField()
            article = models.ForeignKey(Article,
                                        related_name='translations_set')

    We can get translation:

        article = Artcile.objects.get(name='Hello, world!')
        translation = article.get_translation('en')
        
    '''
    def get_translation(self, language):
        if isinstance(language, basestring):
            return self.translations_set.get(language_id=language)
        elif isinstance(language, Language):
            return self.translations_set.get(language=language)
        raise TypeError('%s.get_translation() accepts only string or Language '
                        'argument but %s given' % (self.__class__.__name__,
                                                   type(language)))


class TranslationMixin(object):
    '''Mixin contains field related to language.
    '''
    language = models.ForeignKey(Language, verbose_name=_('Language'))
