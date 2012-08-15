'''Build an admin interface for pages and page-related things
'''
import functools

from django.contrib import admin
from django.core import exceptions, urlresolvers
from django.db import transaction
from django.views.decorators import csrf
from django.utils import decorators, encoding, functional, html
from django.utils.translation import ugettext as _

import forms
import models

csrf_protect_m = decorators.method_decorator(csrf.csrf_protect)


class LanguageAdmin(admin.ModelAdmin):
    '''Class represents admin interface for language model
    '''
    model = models.Language
    list_display = ('name', 'raw_code', )

admin.site.register(models.Language, LanguageAdmin)


class LayoutAdmin(admin.ModelAdmin):
    '''Admin iterface for layouts list
    '''
    model = models.Layout
    list_display = ('name', 'template', 'is_default', 'is_active', )
    fields = ('name', 'template', 'is_default', 'is_active', )

admin.site.register(models.Layout, LayoutAdmin)


class PageAdmin(admin.ModelAdmin):
    '''Class represents admin interface for page model
    '''
    model = models.Page
    add_form_template = 'admin/page_change_form.html'
    change_form_template = 'admin/page_change_form.html'

    @functional.cached_property
    def default_layout(self):
        '''Get default layout
        '''
        return models.Layout.objects.get_default()

    def get_translation_forms(self, data=None):
        '''Get a list of forms for different languages
        '''
        return [forms.PageTranslationForm(data or {}, language=language,
                                initial={'is_active': True,
                                        'layout__id': self.default_layout.id})
                for language in models.Language.objects.all()]

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise exceptions.PermissionDenied

        ModelForm = self.get_form(request)
        if request.method == 'POST':
            # Trying to create new post
            form = ModelForm(request.POST, request.FILES)
            translations = self.get_translation_forms(request.POST)

            if form.is_valid():
                new_object = self.save_form(request, form, change=False)
                form_validated = True
            else:
                form_validated = False
                new_object = self.model()
            transl_valid = functools.reduce(
                            lambda valid, trans: trans.is_valid() and valid,
                            translations, True)
            if form_validated and transl_valid:
                self.save_model(request, new_object, form, True)
                for translation in translations:
                    translation.save(page=new_object)
                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            # Prepare translations
            translations = self.get_translation_forms()
        # Create an admin form
        adminForm = admin.helpers.AdminForm(form,
                                        list(self.get_fieldsets(request)),
                                        self.get_prepopulated_fields(request),
                                        self.get_readonly_fields(request),
                                        model_admin=self)
        media = self.media + adminForm.media

        context = {
            'title': _('Add %s') % encoding.force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': media,
            'errors': admin.helpers.AdminErrorList(form, []),
            'app_label': opts.app_label,
            'translations': translations
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url,
                                       add=True)

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, form_url='', extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, admin.util.unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise exceptions.PermissionDenied

        if obj is None:
            raise exceptions.Http404(
                _('%(name)s object with primary key %(key)r does not exist.') %
                           {'name': encoding.force_unicode(opts.verbose_name),
                            'key': html.escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            url = urlresolvers.reverse('admin:%s_%s_add' %
                                       (opts.app_label, opts.module_name),
                                       current_app=self.admin_site.name)
            return self.add_view(request, form_url=url)

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj

            if form_validated:
                self.save_model(request, new_object, form, True)
                change_message = self.construct_change_message(request, form)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            # Create new form
            form = ModelForm(instance=obj)

        adminForm = admin.helpers.AdminForm(form,
                                    self.get_fieldsets(request, obj),
                                    self.get_prepopulated_fields(request, obj),
                                    self.get_readonly_fields(request, obj),
                                    model_admin=self)
        media = self.media + adminForm.media

        context = {
            'title': _('Change %s') %
                     encoding.force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': media,
            'errors': admin.helpers.AdminErrorList(form, []),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj, form_url=form_url)



admin.site.register(models.Page, PageAdmin)
