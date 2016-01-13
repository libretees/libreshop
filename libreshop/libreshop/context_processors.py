import logging
import re
from django.conf import settings
from django.utils.html import format_html

# Initialize logger.
logger = logging.getLogger(__name__)


def business(request):
    '''
    If this processor is enabled, every RequestContext will contain a variable
    EMAIL_ADDRESS, providing a mailto link generated from the DEFAULT_FROM_EMAIL
    setting, BUSINESS_NAME, LEGAL_NAME, and JURISDICTION.
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
            mailto_link = format_html(
                '<a href=\'mailto:{}\'>{}</a>', email_address, email_address
            )
            context.update({
                'EMAIL_ADDRESS': mailto_link,
            })

    context.update({
        'BUSINESS_NAME': settings.BUSINESS_NAME,
        'LEGAL_NAME': settings.LEGAL_NAME,
        'JURISDICTION': settings.JURISDICTION,
    })

    return context
