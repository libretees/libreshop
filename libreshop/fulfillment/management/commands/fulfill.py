import logging
import signal
import time
import sys
import schedule
from django.core.management.base import BaseCommand, CommandError
from fulfillment.models import Manufacturer
from orders.models import Order, Purchase

# Initialize logger.
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Fulfills the specified order via drop shipment.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.task_queue = dict()


    def add_arguments(self, parser):
        '''
        Set up command line arguments for the management command.
        '''
        parser.add_argument('order_tokens', nargs='*', type=str)
        parser.add_argument(
            '-s', '--server', action='store_true', dest='server'
        )


    def initialize_task_queue(self, manufacturer_name=None):

        manufacturers = (
            Manufacturer.objects.filter(name__in=[manufacturer_name]) or
            Manufacturer.objects.all()
        )

        for manufacturer in manufacturers:

            job = None

            if manufacturer.fulfillment_time:
                scheduled_time = manufacturer.fulfillment_time.strftime('%H:%M')
                logger.debug(
                    'Scheduling fulfillment of (%s) products for (%s)...' %
                    (manufacturer.name, scheduled_time)
                )
                job = schedule.every().day.at(scheduled_time).do(
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
                job = schedule.every(1).seconds.do(
                    self.fulfill_dropship, manufacturer.name
                )
                logger.debug(
                    ('Scheduled fulfillment of (%s) products for every (%s) '
                     'second.') % (manufacturer.name, 1)
                )

            self.task_queue.update({
                manufacturer.name: (job, manufacturer.modified)
            })


    def maintain_task_queue(self):

        manufacturers = Manufacturer.objects.all()

        for manufacturer in manufacturers:
            job_info = self.task_queue.get(manufacturer.name)

            if job_info:
                job, modified_time = job_info

                if modified_time < manufacturer.modified:
                    # Update the run queue with new job schedule information.
                    logger.info(
                        'Rescheduling (%s) fulfillment...' % manufacturer.name
                    )
                    schedule.cancel_job(job)
                    self.initialize_task_queue(manufacturer.name)
                    logger.info(
                        'Rescheduled (%s) fulfillment.' % manufacturer.name
                    )
            else:
                # Add new manufacturers to the run queue.
                self.initialize_task_queue(manufacturer.name)

        # Determine which jobs on run queue should be removed.
        canceled_jobs = {
            name:self.task_queue[name]
            for name in self.task_queue if name not in
            [manufacturer.name for manufacturer in manufacturers]
        }

        # Remove stale entries from the run queue.
        for manufacturer_name, job_info in canceled_jobs.items():
            logger.info(
                'Canceling (%s) fulfillment...' % manufacturer_name
            )

            job, _ = job_info
            schedule.cancel_job(job)
            del self.task_queue[manufacturer_name]

            logger.info(
                'Canceled (%s) fulfillment.' % manufacturer_name
            )


    def server_callback(self, *args, **options):
        logger.info('Fulfillment server starting...')

        self.initialize_task_queue()

        while True:
            self.maintain_task_queue()
            schedule.run_pending()

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
            self.fulfill_orders(tokens=tokens)

        # Enter the server loop if the '--server' option was specified.
        if server:
            # Set up SIGINT signal to call on ctrl-c.
            signal.signal(
                signal.SIGINT, lambda sig, frame: self.exit_callback()
            )
            self.server_callback(*args, **options)
        else:
            # Fulfill all orders, if no command line arguments were provided.
            self.fulfill_orders()


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
            Order.objects.filter(pk__in=[
                purchase.order.pk
                for purchase in Purchase.objects.filter(fulfilled=False)
            ])
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
            purchases = Purchase.objects.filter(order=order.pk, fulfilled=False)
            for purchase in purchases:
                purchase.fulfilled = True
                purchase.save()

            self.stdout.write(self.style.SUCCESS(
                'Order %s has been fulfilled.' % order.token
            ))
        else:
            logger.info('%s %s fulfilled.' %
                (len(orders), 'Orders were' if len(orders) > 1 else 'Order was')
            )

        logger.info('Processed \'fulfill\' management command...')
