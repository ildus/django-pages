from django.contrib import admin

from models import Language


class LanguageAdmin(admin.ModelAdmin):
    '''Class represents admin interface for language model
    '''
    model = Language
    list_display = ('name', 'raw_code', )

admin.site.register(Language, LanguageAdmin)
