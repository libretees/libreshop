from django.core.management.base import BaseCommand, CommandError
from orders.models import Order

class Command(BaseCommand):

    help = 'Fulfills the specified order via drop shipment'

    def add_arguments(self, parser):
        parser.add_argument('order_id', nargs='+', type=int)


    def handle(self, *args, **options):

        for order_id in options['order_id']:
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                raise CommandError('Order "%s" does not exist' % order_id)

            order.fulfilled = True
            order.save()

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully fulfilled order "%s"' % order_id
                )
            )
