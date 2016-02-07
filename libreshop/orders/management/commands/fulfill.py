from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from orders.models import Order

class Command(BaseCommand):

    help = 'Fulfills the specified order via drop shipment'

    def add_arguments(self, parser):
        parser.add_argument('order_tokens', nargs='*', type=str)


    def handle(self, *args, **options):

        tokens = options['order_tokens']

        orders = (
            Order.objects.filter(token__in=tokens) or
            Order.objects.filter(fulfilled=False)
        )

        if len(orders) != len(tokens):
            for token in tokens:
                try:
                    order = Order.objects.get(token=token)
                except Order.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        'Order \'%s\' was specified but does not exist.' % token
                    ))

        if not orders:
            self.stdout.write(self.style.NOTICE(
                'No orders were fulfilled.'
            ))

        for order in orders:
            order.fulfilled = True
            order.save()

            self.stdout.write(self.style.SUCCESS(
                'Order %s has been fulfilled.' % order.token
            ))
