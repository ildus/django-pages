from django.db import models
from django.utils.translation import get_language_info, ugettext_lazy as _


class ActivityMixin(models.Model):
    '''Mixin contains active field
    '''
    active = models.BooleanField(verbose_name=_('Is active'), default=True)

    class Meta:
        abstract = True


class HTMLMetaMixin(models.Model):
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

    class Meta:
        abstract = True


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
        return self.name

    def __unicode__(self):
        '''Get language name for it's code
        '''
        return self.name

    def __repr__(self):
        '''Represent
        '''
        return ''.join(('<', self.__class__.__name__, ': "', self.code, '">'))

    @property
    def info(self):
        return get_language_info(self.code)

    @property
    def name(self):
        return self.info['name']


class NavigationMixin(models.Model):
    '''
    '''
    alias = models.SlugField(verbose_name=_('Alias'), unique=False,
                             help_text=_('URL string alias (slug)'))
    header = models.CharField(max_length=255, verbose_name=_('Header'),
                              blank=True, help_text=_('H1 page tag'))

    class Meta:
        abstract = True


class TranslatedMixin(models.Model):
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

    class Meta:
        abstract = True

    def get_translation(self, language):
        if isinstance(language, basestring):
            return self.translations_set.get(language_id=language)
        elif isinstance(language, Language):
            return self.translations_set.get(language=language)
        raise TypeError('%s.get_translation() accepts only string or Language '
                        'argument but %s given' % (self.__class__.__name__,
                                                   type(language)))


class TranslationMixin(models.Model):
    '''Mixin contains field related to language.
    '''
    language = models.ForeignKey(Language, verbose_name=_('Language'))

    class Meta:
        abstract = True
