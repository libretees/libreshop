import logging
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

# Initialize logger.
logger = logging.getLogger(__name__)


class UniqueTogetherFormSet(BaseInlineFormSet):
    '''
    Properly validate 'unique together' fields within a FormSet.

    This extends the :class:`~django.forms.models.BaseInlineFormSet` object that
    is the default FormSet used on :class:`~django.contrib.admin.TabularInline`
    and :class:`~django.contrib.admin.StackedInline`.
    '''

    def clean(self):
        # Call 'clean' method of the superclass.
        super(UniqueTogetherFormSet, self).clean()

        # Get 'unique together' fields from the Model _meta API.
        unique_together = self.model._meta.unique_together

        # Loop through all of the Form values in the FormSet.
        formset_values = []
        for form in self.forms:
            for fields in unique_together:
                # Convert Form values for 'unique together' fields into a tuple.
                form_values = tuple(
                    form.cleaned_data[field] for field in fields
                )

                # Raise an exception if these values have already been seen.
                if form_values in formset_values:
                    logger.debug(
                        'Have already seen (%s) value! Raising exception...' %
                        ', '.join(repr(value) for value in form_values)
                    )
                    raise ValidationError(
                        '%s in a set must be unique.' %
                        self.model._meta.verbose_name_plural.title(),
                        code='duplicate_values'
                    )
                else:
                    logger.debug(
                        'Have not seen (%s) value.' %
                        ', '.join(repr(value) for value in form_values)
                    )

                # Add Form values to the list of seen FormSet values.
                formset_values.append(form_values)
