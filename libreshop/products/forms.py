import re
import logging
from xml.etree import ElementTree
from django import forms
from django.contrib import admin
from django.db.models.fields.related import OneToOneRel
from django.utils.safestring import mark_safe

from .models import Product, Variant

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
    variants = forms.ModelMultipleChoiceField(queryset=None,
                                              widget=admin.widgets.FilteredSelectMultiple('Variants', False),
                                              required=False)

    def __init__(self, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)
        self.fields['variants'].queryset = Variant.objects.filter(product=self.instance)
        self.initial['variants'] = Variant.objects.filter(product=self.instance)
        relation = OneToOneRel(field=Product,
                               to=Variant,
                               field_name='id')

        prepopulated_values = [('product', self.instance.pk)]
        self.fields['variants'].widget = RelatedFieldWidgetWrapper(self.fields['variants'].widget,
                                                                   relation,
                                                                   admin.site,
                                                                   prepopulated_values)

    def save(self, *args, **kwargs):
        instance = super(ProductChangeForm, self).save(*args, **kwargs)

        if instance.pk:
            for variant in [variant for variant in Variant.objects.filter(product=instance.pk)]:
                if variant not in self.cleaned_data['variants']:
                    # remove a variant that has been unselected
                    Variant.objects.get(id=variant.id).delete()

        return instance

    class Meta:
        model = Product
        fields = ('sku',)


class ProductCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ('sku',)
