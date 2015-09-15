# Import Python module(s)
import string
import time
import random
import base64
import hashlib
import logging

from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe

from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha

# Initialize logger
logger = logging.getLogger(__name__)

class TokenInput(widgets.HiddenInput):

    def __init__(self, attrs=None):
        super(TokenInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):

        token_hash_object = hashlib.sha256(value.encode())
        hashed_value = token_hash_object.hexdigest()

        # Convert 'attrs' dict into HTML attributes.
        final_attrs = ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs.items()])
        html = '<input type="hidden" name="%s" value="%s" %s/>' % (name, hashed_value, final_attrs)

        html += self.render_image(name, value, attrs) + self.render_audio(name, value, attrs)

        return mark_safe(html)

    def render_image(self, name, value, attrs=None):
        # Create an encoded image CAPTCHA.
        captcha_generator = ImageCaptcha()
        image_buffer = captcha_generator.generate(value)
        encoded_image = ('data:image/png;base64,%s' %
                    base64.b64encode(image_buffer.getvalue()).decode())

        # Convert 'attrs' dict into HTML attributes.
        final_attrs = ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs.items()])
        html = '<img name="%s" src="%s" %s/>' % (name, encoded_image, final_attrs)
        return mark_safe(html)

    def render_audio(self, name, value, attrs=None):
        # Create an encoded audio CAPTCHA.
        captcha_generator = AudioCaptcha()
        audio_buffer = captcha_generator.generate(value)

        encoded_audio = ('data:audio/wav;base64,%s' %
                            base64.encodestring(audio_buffer).decode())

        # Convert 'attrs' dict into HTML attributes.
        final_attrs = ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs.items()])
        html = '<audio name="%s" src="%s" %s controls></audio>' % (name, encoded_audio, final_attrs)

        return mark_safe(html)

class CaptchaWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):

        # Create the secret token.
        token = None
        if not settings.DEBUG:
            seed = random.Random(int(round(time.time() * 1000)))
            random.seed(seed)
            self.token = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(6))
        else:
            self.token = '1234'

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
            raise NotImplementedError("This should not happen.")
        return [None, self.token]

    def compress(self, data_list):
        return ' '.join(data_list)

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)
