from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet


class UniqueTogetherFormSet(BaseInlineFormSet):

    def clean(self):

        unique_together = self.model._meta.unique_together

        formset_values = []
        for form in self.forms:
            for fields in unique_together:
                form_values = tuple(
                    form.cleaned_data[field] for field in fields
                )
                if form_values in formset_values:
                    raise ValidationError(
                        '%s in a set must be unique.' %
                        self.model._meta.verbose_name_plural.title()
                    )
                formset_values.append(form_values)
