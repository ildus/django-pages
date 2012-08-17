'''View that renders the page
'''
from django import shortcuts, template

from . import models


def page_view(request, slug=None):
    '''Render a page template with a content
    '''
    page = (models.PageTranslation.objects.get(alias=slug, is_active=True)
            if slug
            else models.PageTranslation.objects.get(page__is_default=True))
    template_name = page.layout.template
    articles = models.PageArticle.objects.filter(page=page,
                            layout=page.layout).select_related('place_alias')
    blocks = {article.place.alias: article for article in articles}
    pages = models.PageTranslation.objects.filter(is_active=True)
    return shortcuts.render_to_response(template_name,
                            {'page': page, 'blocks': blocks, 'pages': pages},
                            context_instance=template.RequestContext(request))
