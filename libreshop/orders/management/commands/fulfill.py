import logging
import signal
import time
import sys
import schedule
from django.core.management.base import BaseCommand, CommandError
from orders.models import Order
from products.models import Manufacturer

# Initialize logger.
logger = logging.getLogger(__name__)

SECONDS_IN_DAY = 86400


class Command(BaseCommand):

    help = 'Fulfills the specified order via drop shipment.'

    def add_arguments(self, parser):
        '''
        Set up command line arguments for the management command.
        '''
        parser.add_argument('order_tokens', nargs='*', type=str)
        parser.add_argument(
            '-s', '--server', action='store_true', dest='server'
        )


    def server_callback(self, *args, **options):
        logger.info('Fulfillment server starting...')

        manufacturers = Manufacturer.objects.all()

        for manufacturer in manufacturers:
            if manufacturer.fulfillment_time:
                scheduled_time = manufacturer.fulfillment_time.strftime('%H:%M')
                logger.debug(
                    'Scheduling fulfillment of (%s) products for (%s)...' %
                    (manufacturer.name, scheduled_time)
                )
                schedule.every().day.at(scheduled_time).do(
                    self.fulfill_dropship, manufacturer.name
                )
                logger.debug(
                    'Scheduled fulfillment of (%s) products for (%s).' %
                    (manufacturer.name, scheduled_time)
                )
            else:
                logger.debug(
                    ('Scheduling fulfillment of (%s) products for every (%s) '
                     'second...') % (manufacturer.name, 1)
                )
                schedule.every(1).seconds.do(
                    self.fulfill_dropship, manufacturer.name
                )
                logger.debug(
                    ('Scheduled fulfillment of (%s) products for every (%s) '
                     'second.') % (manufacturer.name, 1)
                )

        while True:
            logger.debug('Fulfillment server loop starting...')

            schedule.run_pending()

            logger.debug('Fulfillment server loop finished.')

            # Sleep for one second.
            time.sleep(1)


    def exit_callback(self, *args, **options):
        logger.info('Fulfillment server exiting...')
        sys.exit(0)


    def handle(self, *args, **options):
        '''
        Handle management command processing.
        '''
        logger.info('Processing \'fulfill\' management command...')

        # Get command line arguments from 'options' dict.
        server = options['server']
        tokens = options['order_tokens']

        logger.debug('Received the following arguments...')
        logger.debug(options)

        # Fulfill any orders specified on the command line.
        if tokens:
            self.fulfill_orders(tokens)

        # Enter the server loop if the '--server' option was specified.
        if server:
            # Set up SIGINT signal to call on ctrl-c.
            signal.signal(
                signal.SIGINT, lambda sig, frame: self.exit_callback()
            )
            self.server_callback(*args, **options)


    def fulfill_dropship(self, manufacturer_name):
        logger.info(
            'Fulfilling products manufactured by (%s)...' % manufacturer_name
        )
        logger.info(
            'Fulfilled products manufactured by (%s).' % manufacturer_name
        )


    def fulfill_orders(self, tokens=[]):

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
