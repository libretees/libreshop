import datetime
import signal
from decimal import Decimal
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO
from orders.models import Order, Purchase
from products.models import Product, Variant
from ..management.commands import fulfill
from ..models import FulfillmentSetting, FulfillmentSettingValue, Supplier
try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch


class FulfillCommandLineTest(TestCase):

    def setUp(self):

        # Set up string buffer to capture command output.
        self.output = StringIO()

        # Set up test data.
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )
        self.order = Order.objects.create()
        purchase = Purchase.objects.create(order=self.order, variant=variant)
        self.order2 = Order.objects.create()
        purchase = Purchase.objects.create(order=self.order2, variant=variant)


    def test_command_output_when_invalid_order_specified(self):

        # Simulate no orders available for fulfillment.
        Order.objects.all().delete()

        call_command(
            'fulfill', stdout=self.output, order_tokens=['foo']
        )

        expected_output = 'Order \'foo\' was specified but does not exist.'

        self.assertIn(expected_output, self.output.getvalue())


    def test_command_output_when_no_orders_are_fulfilled(self):

        # Simulate no orders available for fulfillment.
        Order.objects.all().delete()

        call_command('fulfill', stdout=self.output)
        self.assertIn('No orders were fulfilled!', self.output.getvalue())


    def test_command_output_when_all_orders_are_fulfilled(self):

        call_command('fulfill', stdout=self.output)
        self.assertIn('Fulfilled Order', self.output.getvalue())


    def test_command_result_when_all_orders_are_fulfilled(self):

        call_command('fulfill', stdout=self.output)

        result = all(order.fulfilled for order in Order.objects.all())
        self.assertTrue(result)


    def test_command_output_for_a_specific_order(self):

        call_command(
            'fulfill', stdout=self.output, order_tokens=[self.order.token]
        )

        expected_output = 'Fulfilled Order %s.' % self.order.token

        self.assertIn(expected_output, self.output.getvalue())


    def test_command_result_for_a_specific_order(self):

        call_command(
            'fulfill', stdout=self.output, order_tokens=[self.order.token]
        )

        result = self.order.fulfilled and not self.order2.fulfilled

        self.assertTrue(result)


    @patch.object(fulfill.Command, 'server_callback')
    def test_command_server_flag_intializes_a_server(self, server_callback_mock):

        call_command('fulfill', stdout=self.output, server=True)

        self.assertTrue(server_callback_mock.called)


    @patch.object(fulfill.signal, 'signal')
    @patch.object(fulfill.Command, 'server_callback')
    def test_server_sets_up_a_sigint_callback(self, server_callback_mock, signal_callback):
        call_command('fulfill', stdout=self.output, server=True)
        args, kwargs = signal_callback.call_args
        self.assertIn(signal.SIGINT, args)


    @patch.object(fulfill, 'DaemonContext')
    @patch.object(fulfill.Command, 'server_callback')
    def test_command_daemon_flag_intializes_a_daemon(self, server_callback_mock, daemon_context_mock):

        call_command('fulfill', stdout=self.output, daemon=True)

        self.assertTrue(daemon_context_mock.called)


class FulfillServerTest(TestCase):

    def setUp(self):

        # Set up test data.
        self.supplier = Supplier.objects.create(
            name='foo',
            fulfillment_backend='django.core.mail.backends.locmem.EmailBackend',
            fulfillment_time=timezone.now() + datetime.timedelta(minutes=1)
        )
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='bar'
        )
        to_address_setting = FulfillmentSetting.objects.create(
            supplier=self.supplier, name='to_address'
        )
        subject_setting = FulfillmentSetting.objects.create(
            supplier=self.supplier, name='subject'
        )
        body_setting = FulfillmentSetting.objects.create(
            supplier=self.supplier, name='body'
        )
        to_address_value = FulfillmentSettingValue.objects.create(
            setting=to_address_setting, variant=variant, value='foo@example.com'
        )
        subject_value = FulfillmentSettingValue.objects.create(
            setting=subject_setting, variant=variant, value='Bar'
        )
        body_value = FulfillmentSettingValue.objects.create(
            setting=body_setting, variant=variant, value=(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed '
                'do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
            )
        )
        self.order = Order.objects.create()
        self.purchase = Purchase.objects.create(
            order=self.order, variant=variant
        )

        # Set up management command.
        self.command = fulfill.Command()

        # Route management command output to string buffer.
        self.output = StringIO()
        self.command.stdout = self.output


    def test_server_has_empty_task_queue_when_no_suppliers_are_present(self):
        # Delete the Supplier created in self.setUp.
        self.supplier.delete()
        self.command.server_callback(test=True)
        self.assertEqual(self.command.task_queue, {})


    def test_server_has_continuous_job_in_task_queue_when_no_fulfillment_time_specified(self):

        # Simulate a non-specified fulfillment time.
        self.supplier.fulfillment_time = None
        self.supplier.save()

        self.command.server_callback(test=True)

        job, _ = self.command.task_queue['foo']

        self.assertEqual((job.interval, job.unit), (1, 'seconds'))


    def test_server_has_scheduled_job_in_task_queue_when_fulfillment_time_specified(self):

        self.command.server_callback(test=True)

        job, _ = self.command.task_queue['foo']

        expected_scheduled_time = (
            1, 'days', self.supplier.fulfillment_time.strftime('%H:%M')
        )
        actual_scheduled_time = (
            job.interval, job.unit, job.at_time.strftime('%H:%M')
        )

        self.assertEqual(expected_scheduled_time, actual_scheduled_time)


    def test_server_adds_job_to_task_queue_when_new_supplier_is_added(self):

        # Simulate initial server loop.
        self.command.server_callback(test=True)

        # Add new supplier.
        supplier2 = Supplier.objects.create(
            name='bar',
            fulfillment_backend='django.core.mail.backends.locmem.EmailBackend',
            fulfillment_time=timezone.now() + datetime.timedelta(minutes=1)
        )

        # Simulate secondary server loop.
        self.command.server_callback(test=True)

        self.assertIn('bar', self.command.task_queue)



    def test_server_reschedules_job_in_task_queue_when_it_is_modified(self):

        # Simulate initial server loop.
        self.command.server_callback(test=True)

        # Simulate a modified fulfillment time.
        self.supplier.fulfillment_time += datetime.timedelta(hours=1)
        self.supplier.modified += datetime.timedelta(hours=1)
        self.supplier.save()

        # Simulate secondary server loop.
        self.command.server_callback(test=True)

        job, _ = self.command.task_queue['foo']

        expected_scheduled_time = (
            1, 'days', self.supplier.fulfillment_time.strftime('%H:%M')
        )
        actual_scheduled_time = (
            job.interval, job.unit, job.at_time.strftime('%H:%M')
        )

        self.assertEqual(expected_scheduled_time, actual_scheduled_time)


    def test_server_removes_job_from_task_queue_when_supplier_is_deleted(self):

        # Simulate initial server loop.
        self.command.server_callback(test=True)

        # Delete supplier.
        self.supplier.delete()

        # Simulate secondary server loop.
        self.command.server_callback(test=True)

        self.assertNotIn('foo', self.command.task_queue)


    @patch.object(fulfill.time, 'sleep')
    def test_server_sleeps_between_loop_iterations(self, sleep_mock):

        sleep_mock.side_effect = ValueError()

        # Simulate normal server loop.
        self.assertRaises(ValueError, self.command.server_callback)


    @patch.object(fulfill.sys, 'exit')
    def test_server_can_gracefully_terminate(self, exit_mock):

        # Simulate server termination.
        self.command.exit_callback()

        self.assertTrue(exit_mock.called)


    @patch('django.core.mail.backends.locmem.EmailBackend')
    def test_server_does_nothing_if_there_are_no_purchases_to_fulfill(self, backend_mock):
        self.purchase.delete()
        self.command.fulfill_dropship('foo')
        self.assertFalse(backend_mock.called)


    @patch('django.core.mail.backends.locmem.EmailBackend')
    def test_server_does_not_fulfill_order_if_backend_returns_nothing(self, backend_mock):
        backend_mock.return_value = None
        self.assertFalse(self.order.fulfilled)


    @patch('django.core.mail.backends.locmem.EmailBackend')
    def test_server_can_fulfill_drop_shipment_orders(self, backend_mock):

        backend_mock.return_value = {
            'id': 'foo',
            'subtotal': Decimal(0.00),
            'shipping_cost': Decimal(0.00),
            'tax': Decimal(0.00),
            'fees': Decimal(0.00),
            'total': Decimal(0.00),
            'created_at': timezone.now(),
            'line_items': [{
                'purchase': self.purchase,
                'subtotal': Decimal(0.00),
                'shipping_cost': Decimal(0.00),
                'tax': Decimal(0.00),
                'fees': Decimal(0.00),
                'total': Decimal(0.00)
            }]
        }

        self.command.fulfill_dropship('foo')

        self.assertTrue(self.order.fulfilled)
