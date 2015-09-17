# Import Python module(s)

import logging

from django.forms import widgets
from django.utils.safestring import mark_safe

# Initialize logger
logger = logging.getLogger(__name__)


class TokenInput(widgets.HiddenInput):

    def __init__(self, attrs=None):
        super(TokenInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # Defer import of RegistrationToken to resolve interdependency with forms module.
        from .forms import RegistrationToken
        self.registration_token = RegistrationToken()

        # Convert 'attrs' dict into HTML attributes.
        final_attrs = ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs.items()])

        # Render HTML.
        html = '''<input type="hidden" name="%s" value="%s" %s/>
                  <img name="%s" src="%s" %s/>
                  <audio name="%s" src="%s" %s controls></audio>
               ''' % (name, self.registration_token.token, final_attrs,
                      name, self.registration_token.image, final_attrs,
                      name, self.registration_token.audio, final_attrs)

        return mark_safe(html)


class CaptchaWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):

        widgets_ = (
            widgets.TextInput(attrs=attrs),
            TokenInput(attrs=attrs),
        )
        super(CaptchaWidget, self).__init__(widgets_, attrs)

    def render(self, name, value, attrs=None):
        # HTML to be added to the output

        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        # value is a list of values, each corresponding to a widget in self.widgets
        if not isinstance(value, list):
            value = self.decompress(value)

        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))

            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))

        return mark_safe(self.format_output(output))

    def decompress(self, value):
        if value:
            value.split(':')
        return [None, None]

    def compress(self, data_list):
        return ' '.join(data_list)

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)
