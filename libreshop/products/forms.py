import re
import logging
from xml.etree import ElementTree
from django import forms
from django.forms.widgets import Select, Textarea
from django.forms.utils import ErrorList
from django.contrib import admin
from django.db.models.fields.related import OneToOneRel
from django.utils.safestring import mark_safe
from . import models

# Initialize logger
logger = logging.getLogger(__name__)

class RelatedFieldWidgetWrapper(admin.widgets.RelatedFieldWidgetWrapper):

    def __init__(self, widget, rel, admin_site, values, can_add_related=None,
        can_change_related=False, can_delete_related=False):

        super(RelatedFieldWidgetWrapper, self).__init__(widget, rel, admin_site,
            can_add_related, can_change_related, can_delete_related)

        self.values = values


    def render(self, name, value, *args, **kwargs):
        html = super(RelatedFieldWidgetWrapper, self).render(name, value, *args,
            **kwargs)

        if self.can_add_related:
            extra_args = '&'.join("%s=%s" % param for param in self.values)

            xml = ElementTree.fromstring(html)
            link_id = 'add_id_%s' % self.rel.to._meta.verbose_name_plural
            anchor_tag = xml.find('.//a[@id="%s"]' % link_id)
            href = anchor_tag.get('href', '')
            query_string = bool(re.search(r'\?+', href))
            href += ('&' if query_string else '?') + extra_args
            anchor_tag.set('href', href)
            html = ElementTree.tostring(xml)

        return mark_safe(html)


class ProductChangeForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ('sku', 'name', 'description', 'image',)
        widgets = {'description': Textarea(attrs={'cols': 80, 'rows': 5})}


    variants = forms.ModelMultipleChoiceField(
        label='Enabled Variants',
        widget=admin.widgets.FilteredSelectMultiple('Variants', False),
        required=False,
        queryset=None
    )


    def __init__(self, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)

        self.fields['variants'].queryset = (
            models.Variant.objects. filter(product=self.instance)
        )

        self.initial['variants'] = models.Variant.objects.filter(
                product=self.instance, enabled=True
        )

        relation = OneToOneRel(
            field=models.Product, to=models.Variant, field_name='id'
        )

        prepopulated_values = [('product', self.instance.pk)]

        self.fields['variants'].widget = RelatedFieldWidgetWrapper(
            self.fields['variants'].widget,
            relation,
            admin.site,
            prepopulated_values
        )


    def save(self, *args, **kwargs):

        instance = super(ProductChangeForm, self).save(*args, **kwargs)

        if instance.pk:

            enabled_variants = ([
                variant for variant in
                models.Variant.objects.filter(product=instance.pk, enabled=True)
            ])

            # Disable a Variant that has been unselected.
            for variant in enabled_variants:
                if variant not in self.cleaned_data['variants']:
                    variant = models.Variant.objects.get(id=variant.id)
                    variant.enabled = False
                    variant.save()

            # Enable a Variant that has been selected.
            for variant in self.cleaned_data['variants']:
                if variant not in enabled_variants:
                    variant = models.Variant.objects.get(id=variant.id)
                    variant.enabled = True
                    variant.save()

        return instance


class ProductCreationForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ('sku', 'name')


    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)


class VariantCreationForm(forms.ModelForm):

    class Meta:
        model = models.Variant
        fields = ('product', 'name', 'sub_sku', 'price')


def PopulatedFormFactory(request, cls, form=forms.ModelForm):

    model_field_names = [_.name for _ in cls._meta.get_fields()]

    class PopulatedForm(form):
        def __init__(self, *args, **kwargs):
            super(PopulatedForm, self).__init__(*args, **kwargs)
            if request.method in ['GET', 'POST']:
                for key in request.GET:
                    try:
                        field = self.fields[key]
                        field.required = False
                        if isinstance(field, forms.models.ModelChoiceField):
                            field.empty_label = None
                            related_model_name = (field.queryset.model._meta
                                .model_name.title())
                            cls = getattr(models, related_model_name, None)
                            if cls:
                                object_id = request.GET[key]
                                field.widget = (Select(
                                    attrs={'disabled': 'disabled'}))
                                field.queryset = (cls.objects.
                                    filter(id=object_id))
                        else:
                            field.widget.attrs['readonly'] = True
                            field.widget.attrs['disabled'] = 'disabled'
                    except KeyError:
                        # Ignore unexpected parameters
                        pass


    def get_clean_function(name):
        def func(self):
            value = None
            field = self.fields[name]
            if isinstance(field, forms.models.ModelChoiceField):
                related_model = field.queryset.model
                value = related_model.objects.get(id=request.GET[name])
            else:
                value = request.GET[name]
            return value
        return func

    for key in [key for key in request.GET if key in model_field_names]:
        setattr(PopulatedForm, 'clean_%s' % key, get_clean_function(key))

    return PopulatedForm


class ProductOrderForm(forms.Form):


    def __init__(self, product, **kwargs):
        super(ProductOrderForm, self).__init__(**kwargs)

        for key, values in product.attributes.items():
            choices = [(value, value) for value in values]
            if len(choices) > 1:
                choices.insert(0, ('', 'Choose a %s' % key))
                self.fields[key] = forms.fields.ChoiceField(choices=choices)


    def __str__(self):
        return self.as_div()


    def as_div(self):
        '''
        Returns this form rendered as HTML <div>s.
        '''
        return super(ProductOrderForm, self)._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s %(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)
