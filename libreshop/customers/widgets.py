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


class RegistrationToken(object):
    """
    This creates a registration token that permits a stateless user registration
    with image and audio CAPTCHAs.
    """

    def __init__(self):
        super(RegistrationToken, self).__init__()
        self._generate_token()
        self._generate_image()
        self._generate_audio()

    def _generate_token(self):
        # Create the secret token.
        token = None
        if not settings.DEBUG:
            seed = random.Random(int(round(time.time() * 1000)))
            random.seed(seed)
            token = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(6))
        else:
            token = '1234'

        token_hash_object = hashlib.sha256(token.encode())
        hashed_value = token_hash_object.hexdigest()

        self.token = token
        self.value = hashed_value

    def _generate_image(self):
        # Create an encoded image CAPTCHA.
        captcha_generator = ImageCaptcha()
        image_buffer = captcha_generator.generate(self.token)
        encoded_image = ('data:image/png;base64,%s' %
                            base64.b64encode(image_buffer.getvalue()).decode())

        self.image = encoded_image

    def _generate_audio(self):
        # Create an encoded audio CAPTCHA.
        captcha_generator = AudioCaptcha()
        audio_buffer = captcha_generator.generate(self.token)
        encoded_audio = ('data:audio/wav;base64,%s' %
                            base64.encodestring(audio_buffer).decode())

        self.audio = encoded_audio


class TokenInput(widgets.HiddenInput):

    def __init__(self, attrs=None):
        super(TokenInput, self).__init__(attrs)
        self.token = RegistrationToken()

    def render(self, name, value, attrs=None):
        # Convert 'attrs' dict into HTML attributes.
        final_attrs = ' '.join(['%s="%s"' % (key, value) for (key, value) in attrs.items()])

        # Render HTML.
        html = '''<input type="hidden" name="%s" value="%s" %s/>
                  <img name="%s" src="%s" %s/>
                  <audio name="%s" src="%s" %s controls></audio>
               ''' % (name, self.token.value, final_attrs,
                      name, self.token.image, final_attrs,
                      name, self.token.audio, final_attrs)

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
