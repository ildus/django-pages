"""This file contains test for pages models and mixins. 

TODO: split test into different files to make it easier to understand and modify
"""
from django.test import TestCase

from pages import mixins, models


class TranslationMixinTest(TestCase):
    '''Test case for translatation and translated mixin
    '''

    def test_language(self):
        '''Create new language and check it's properties
        '''
        english = mixins.Language.objects.create(code='en')
        self.assertEqual(english.code, 'en')
        self.assertEqual(repr(english), '<Language: "en">')
        self.assertEqual(str(english), 'English')
        self.assertEqual(unicode(english), 'English')
        self.assertEqual(english.name, 'English')
        self.assertEqual(english.info, {'code': 'en', 'name_local': u'English',
                                        'bidi': False, 'name': 'English'})

    def test_get_translation(self):
        """Test get_translation() method from TranslatedMixin class
        """
        english = mixins.Language.objects.create(code='en')
        russian = mixins.Language.objects.create(code='ru')
        page = models.Page.objects.create()
        models.PageTranslation.objects.create(page=page, title='Hello, USA',
                                              language=english)
        models.PageTranslation.objects.create(page=page, title='Hello, Russia',
                                              language=russian)
        translatation = page.get_translation(english)
        self.assertEqual(translatation.language, english)
        self.assertEqual(translatation.page, page)
        self.assertEqual(translatation.title, 'Hello, USA')
        translatation = page.get_translation(russian.code)
        self.assertEqual(translatation.language, russian)
        self.assertEqual(translatation.page, page)
        self.assertEqual(translatation.title, 'Hello, Russia')
