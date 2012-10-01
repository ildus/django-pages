'''Tags for menu
'''


'''Some tags for the news application
'''
from django import template
from django.conf import settings

from .. import models

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_items(context, var_name, alias):
    '''Put a list of menu items related to menu with specified alias into
    context with selected variable name
    '''
    menu = models.Menu.objects.get(alias=alias)
    pages = models.MenuItem.objects.filter(menu=menu).values_list('page_id',
                                                flat=True).order_by('order')
    page_ids = [page_id for page_id in pages]
    order = {page_id: index for index, page_id in enumerate(page_ids)}
    language = models.Language.objects.filter(code=settings.LANGUAGE_CODE)
    translations = models.PageTranslation.objects.filter(language=language,
                                                         page_id__in=pages)
    translations_map = {order[transl.id]: transl
                        for transl in translations}
    context[var_name] = [translations_map[index] for index in range(len(page_ids))]
    return ''
