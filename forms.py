'''Forms for pages
'''
import re

import unidecode

from django import forms

from tinymce.widgets import TinyMCE

import models


def slugify(text):
    '''Get a slug of a text
    '''
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', '-', text)


class PageTranslationForm(forms.ModelForm):
    '''Form for translations
    '''

    def __init__(self, *args, **kwargs):
        '''Create PageTranslationForm.

        Request language attribute and also accepts optional object attribute.
        They would be used on oblect saving
        '''
        # Get language and page
        self.language = kwargs['language']
        del kwargs['language']
        kwargs['prefix'] = self.language.raw_code
        if 'page' in kwargs:
            self.page = kwargs['page']
            del kwargs['page']
        else:
            self.page = None
        # Create form
        super(PageTranslationForm, self).__init__(*args, **kwargs)
        self.fields['title_tag'].required = True  # Requred

    @property
    def layout(self):
        '''Shourtcut for getting layout
        '''
        if hasattr(self, 'cleaned_data') and 'layout' in self.cleaned_data:
            return models.Layout.objects.get(id=self.cleaned_data['layout'])
        else:
            return None

    def clean(self):
        '''Set default values
        '''
        cleaned_data = super(PageTranslationForm, self).clean()
        if not cleaned_data.get('title', None):
            cleaned_data['title'] = cleaned_data['title_tag']
        if not cleaned_data.get('header', None):
            cleaned_data['header'] = cleaned_data['title_tag']
        if not cleaned_data.get('alias', None):
            cleaned_data['alias'] = cleaned_data['title_tag']
        return self.cleaned_data

    def save(self, commit=True, page=None):
        '''Save object
        '''
        # Not commits yet
        translation = super(PageTranslationForm, self).save(commit=False)
        # Update translation with language and page
        translation.language = self.language
        translation.page = page or self.page
        if commit:  # Commit changes if needed
            translation.save()
        return translation

    FIELD_GROUPS = (
        ('title_tag', 'layout', 'active', ),
        ('header', 'title', 'alias', ),
        ('meta_description', 'meta_keywords', )
    )

    def fieldsets(self):
        '''Group fields into fieldsets
        '''
        print 'Get a fieldsets'
        fieldsets = {}
        for field in self:
            print field
            index = 0
            for group in PageTranslationForm.FIELD_GROUPS:
                index += 1
                if field.name in group:
                    if index in fieldsets:
                        fieldsets[index].append(field)
                    else:
                        fieldsets[index] = [field]
        print fieldsets, [fieldsets[index] for index in fieldsets]
        return [fieldsets[index] for index in fieldsets]

    class Meta:
        model = models.PageTranslation
        exclude = ('language', 'page', )  # Set them manually


class PageContentForm(forms.ModelForm):
    '''Form for page content
    '''

    def __init__(self, *args, **kwargs):
        '''Build new forms includes
        '''
        # Get arguments
        self.layout = kwargs['layout']
        del kwargs['layout']
        self.place = kwargs['place']
        del kwargs['place']
        if 'page' in kwargs:
            self.page = kwargs['page']
            del kwargs['page']
        else:
            self.page = None
        kwargs['prefix'] = '-'.join([kwargs['language'].raw_code,
                                     str(self.layout.pk), str(self.place.pk)])
        del kwargs['language']
        kwargs['initial'] = kwargs.get('initial', {'is_active': True})
        # Create form
        super(PageContentForm, self).__init__(*args, **kwargs)
        # Update a widget
        self.fields['text'].widget = TinyMCE()

    def save(self, commit=True, page=None):
        '''Save object
        '''
        # Not commits yet
        content = super(PageContentForm, self).save(commit=False)
        # Update content block with language and page
        content.layout = self.layout
        content.page = page or self.page
        content.place = self.place
        if commit:  # Commit changes if needed
            content.save()
        return content

    class Meta:
        model = models.PageArticle
        exclude = ('layout', 'page', 'place', )  # Set them manually
