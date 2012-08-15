'''Forms for pages
'''
from django import forms

import models


class PageTranslationForm(forms.ModelForm):
    '''Form for translations
    '''

    class Meta:
        model = models.PageTranslation
        exclude = ('', )
