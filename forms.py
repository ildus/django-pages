'''Forms for pages
'''
from django import forms

from tinymce.widgets import TinyMCE

import models


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
