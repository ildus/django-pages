"""This file contains test for pages models and mixins. 

TODO: split test into different files to make it easier to understand and modify
"""
from django.db import models
from django.test import TestCase

from .mixins import Language, TranslatedMixin, TranslationMixin


class Article(TranslatedMixin):
    name = models.CharField(max_length=255)


class ArticleTranslation(TranslationMixin):
    title = models.CharField(max_length=255)
    content = models.TextField()
    article = models.ForeignKey(Article, related_name='translations_set')


class TranslationMixinTest(TestCase):
    '''Test case for translatation and translated mixin
    '''

    def test_language(self):
        '''Create new language and check it's properties
        '''
        english = Language.objects.create(code='en')
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
        english = Language.objects.create(code='en')
        russian = Language.objects.create(code='ru')
        article = Article.objects.create(name='Hello, world!')
        ArticleTranslation.objects.create(article=article, title='Hello, USA',
                                        content='US English', language=english)
        ArticleTranslation.objects.create(article=article, content='Russian',
                                    title='Hello, Russia', language=russian)
        translatation = article.get_translation(english)
        self.assertEqual(translatation.language, english)
        self.assertEqual(translatation.article, article)
        self.assertEqual(translatation.content, 'US English')
        self.assertEqual(translatation.title, 'Hello, USA')
        translatation = article.get_translation(russian.code)
        self.assertEqual(translatation.language, russian)
        self.assertEqual(translatation.article, article)
        self.assertEqual(translatation.content, 'Russian')
        self.assertEqual(translatation.title, 'Hello, Russia')
