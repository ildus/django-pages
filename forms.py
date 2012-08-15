'''Forms for pages
'''
from django import forms

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
        if 'page' in kwargs:
            self.page = kwargs['page']
            del kwargs['page']
        else:
            self.page = None
        # Create form
        super(PageTranslationForm, self).__init__(*args, **kwargs)
        self.fields['title_tag'].required = True  # Requred

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
