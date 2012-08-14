from django.contrib import admin

import models


class LanguageAdmin(admin.ModelAdmin):
    '''Class represents admin interface for language model
    '''
    model = models.Language
    list_display = ('name', 'raw_code', )

admin.site.register(models.Language, LanguageAdmin)


class PageAdmin(admin.ModelAdmin):
    '''Class represents admin interface for page model
    '''
    model = models.Page

admin.site.register(models.Page, PageAdmin)
