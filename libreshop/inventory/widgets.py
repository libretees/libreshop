from django import forms
from django.db import models

UNITS_OF_MEASURE = (
    ('bg', 'bag'),
    ('bf', 'board feet'),
    ('bl', 'bale'),
    ('bt', 'bottle'),
    ('bx', 'box'),
    ('c', 'hundred'),
    ('cc', 'cubic centimeter'),
    ('cf', 'cubic feet'),
    ('ci', 'curie'),
    ('cl', 'cylinder'),
    ('cm', 'centimeter'),
    ('cn', 'can'),
    ('cs', 'case'),
    ('ct', 'carton'),
    ('cw', 'hundred weight'),
    ('cy', 'cubic yard'),
    ('di', 'diameter'),
    ('dr', 'drum'),
    ('dw', 'dewar'),
    ('dy', 'day'),
    ('dz', 'dozen'),
    ('ea', 'each'),
    ('ft', 'feet'),
    ('gl', 'gallon'),
    ('gm', 'gram'),
    ('gn', 'grain'),
    ('gr', 'gross'),
    ('hr', 'hour'),
    ('in', 'inch'),
    ('jr', 'jar'),
    ('kg', 'kilogram'),
    ('kt', 'kit'),
    ('la', 'lambda'),
    ('lb', 'pound'),
    ('lf', 'linear feet'),
    ('lg', 'length'),
    ('li', 'liter'),
    ('lt', 'lot'),
    ('ly', 'linear yard'),
    ('m', 'thousand'),
    ('mg', 'milligram'),
    ('ml', 'milliliter'),
    ('mm', 'millimeter'),
    ('mn', 'minute'),
    ('mo', 'month'),
    ('mr', 'micron'),
    ('mt', 'meter'),
    ('og', 'omega'),
    ('oz', 'ounce'),
    ('pa', 'package'),
    ('pc', 'piece'),
    ('pg', 'page'),
    ('pk', 'pack'),
    ('pl', 'pallet'),
    ('pr', 'pair'),
    ('pt', 'pint'),
    ('qr', 'quarter'),
    ('qt', 'quart'),
    ('rd', 'rod'),
    ('rl', 'roll'),
    ('rm', 'ream'),
    ('sf', 'square feet'),
    ('sh', 'sheet'),
    ('st', 'set'),
    ('sy', 'square yard'),
    ('tb', 'tube'),
    ('tr', 'transaction'),
    ('ut', 'unit'),
    ('vl', 'vial'),
    ('wk', 'week'),
    ('yd', 'yard'),
    ('yr', 'year')
)


class ConversionFactorWidget(forms.MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if not widgets:
            read_only_attrs = {
                'readonly': True,
                'disabled': 'disabled'
            }
            widgets = (
                forms.NumberInput(attrs=attrs),
                forms.Select(attrs=attrs, choices=UNITS_OF_MEASURE),
                forms.NumberInput(attrs=attrs),
                forms.Select(attrs=read_only_attrs, choices=UNITS_OF_MEASURE)
            )
        super(ConversionFactorWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        decompressed_values = [None, None, None, None]
        if value:
            decompressed_values = [
                j for i in value.split(':') for j in i.split(' ')]
        return decompressed_values

    def format_output(self, rendered_widgets):
        numerator_widget = ''.join(rendered_widgets[2:])
        denominator_widget = ''.join(rendered_widgets[:2])
        return '%s to %s' % (numerator_widget, denominator_widget)

    class Media:
        js = ('inventory/js/conversion_factor_widget.js',)


class ConversionFactorField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'fields': (
                forms.DecimalField(),
                forms.ChoiceField(choices=UNITS_OF_MEASURE),
                forms.DecimalField(),
                forms.ChoiceField(choices=UNITS_OF_MEASURE),
            ),
            'require_all_fields': True,
            'widget': ConversionFactorWidget
        })
        super(ConversionFactorField, self).__init__(*args, **kwargs)

    def compress(self, data_list):
        compressed_value = None
        if data_list:
            compressed_value = '%f %s:%f %s' % tuple(data_list)
        return compressed_value
