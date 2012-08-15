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

    def save(self, *args, **kwargs):
        '''Save object
        '''
        # Save form but without commiting to database
        commit = kwargs.get('commit', False)
        kwargs['commit'] = False
        translation = super(PageTranslationForm, self).save(*args, **kwargs)
        # Update translation with language and page
        translation.language = self.language
        translation.page = kwargs.get('page', self.page)
        if commit:  # Commit changes if needed
            translation.save()
        return translation

    class Meta:
        model = models.PageTranslation
        exclude = ('language', 'page', )  # Set them manually
