from django.db import models

import mixins

Language = mixins.Language


class Page(mixins.TranslatedMixin):
    '''Page object used to represent object's position inside a site objects
    hierarhy, activity state and can contains translation
    '''
    pass


class PageTranslation(mixins.ActivityMixin, mixins.HTMLMetaMixin,
                      mixins.NavigationMixin, mixins.TranslationMixin):
    '''Represent page translation for current language
    '''
    pass


class PageContent(models.Model):
    '''Element represents page content
    '''
    pass
