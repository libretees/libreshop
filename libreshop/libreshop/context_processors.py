import logging
import re
from django.conf import settings
from django.utils.html import format_html

# Initialize logger.
logger = logging.getLogger(__name__)


def default_from_email(request):
    '''
    If this processor is enabled, every RequestContext will contain a variable
    DEFAULT_FROM_EMAIL, providing the value of the DEFAULT_FROM_EMAIL setting.
    '''
    context = {}
    default_from_email = settings.DEFAULT_FROM_EMAIL

    if default_from_email:
        match = re.search('<(.+?)>', default_from_email)
        try:
            email_address = match.group(1)
        except AttributeError as e:
            logger.error(('Could not extract the email address specified in the'
                ' DEFAULT_FROM_EMAIL setting.'))
        else:
            link = format_html(
                '<a href=\'mailto:{}\'>{}</a>', email_address, email_address
            )
            context.update({
                'DEFAULT_FROM_EMAIL': link,
            })

    return context
