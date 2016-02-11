import logging
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from orders.models import Order

# Initialize logger.
logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = 'Fulfills the specified order via drop shipment.'

    def add_arguments(self, parser):
        '''
        Set up command line arguments for the management command.
        '''
        parser.add_argument('order_tokens', nargs='*', type=str)


    def handle(self, *args, **options):
        '''
        Handle management command processing.
        '''
        logger.info('Processing \'fulfill\' management command...')

        # Get command line arguments from 'options' dict.
        tokens = options['order_tokens']

        # Get Orders by using the Order Token specified on the command line, or
        # get all unfulfilled orders, by default.
        orders = (
            Order.objects.filter(token__in=tokens) or
            Order.objects.filter(fulfilled=False)
        )

        # Check for and report any invalid Order Tokens.
        if len(orders) != len(tokens):
            for token in tokens:
                try:
                    order = Order.objects.get(token=token)
                except Order.DoesNotExist:
                    message = (
                        'Order \'%s\' was specified but does not exist.' % token
                    )
                    logger.warn(message)
                    self.stdout.write(self.style.WARNING(message))

        # Display a warning, if no orders were fulfilled.
        if not orders:
            message = 'No orders were fulfilled!'
            logger.warn(message)
            self.stdout.write(self.style.NOTICE(message))

        # Fullfill orders.
        for order in orders:
            order.fulfilled = True
            order.save()

            self.stdout.write(self.style.SUCCESS(
                'Order %s has been fulfilled.' % order.token
            ))
        else:
            logger.info('%s Orders were fulfilled.' % len(orders))

        logger.info('Processed \'fulfill\' management command...')
