import logging
from django.contrib.gis.geoip2 import GeoIP2
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from ipware.ip import get_real_ip
from addresses.forms import AddressForm

# Initialize logger.
logger = logging.getLogger(__name__)

# Set a universally unique identifier (UUID).
UUID = '9bf75036-ec58-4188-be12-4f983cac7e55'

# Create views here.
class CheckoutFormView(FormView):

    form_class = AddressForm
    template_name = 'orders/checkout.html'
    success_url = '/'

    def __init__(self, *args, **kwargs):
        super(CheckoutFormView, self).__init__(*args, **kwargs)

        self.steps_completed = None
        self.steps_remaining = None
        self.steps = (
            {
                'name': 'shipping_address',
                'form': AddressForm,
                'template': 'orders/checkout.html',
                'context': {
                    'description': 'where are we sending this?',
                }
            },
            {
                'name': 'billing_address',
                'form': AddressForm,
                'template': 'orders/checkout.html',
                'context': {
                    'description': 'who are we billing?',
                }
            },
            {
                'name': 'payment',
                'form': AddressForm,
                'template': 'orders/checkout.html',
                'context': {
                    'description': 'how are you paying?',
                }
            },
        )


    def dispatch(self, request, *args, **kwargs):

        self.current_step = self.get_current_step()

        return super(CheckoutFormView, self).dispatch(request, *args, **kwargs)


    def get_current_step(self):
        '''
        Get the current step within the form wizard.
        '''
        completed_steps = self.request.session.get(UUID, {})

        remaining_steps = [
            step for step in self.steps if step['name'] not in completed_steps
        ]
        current_step = remaining_steps[0] if remaining_steps else None

        logger.debug('Completed steps: %s' % ', '.join(step for step in completed_steps))
        logger.debug('Remaining steps: %s' % ', '.join(step['name'] for step in remaining_steps))
        logger.debug('Current step: %s' % (current_step['name'] if current_step else ''))

        return current_step


    def get_template_names(self):
        template_name = self.current_step['template']

        return [template_name]


    def get_form_class(self):
        return self.current_step['form']


    def get_form(self):
        '''
        Get the Form object that will be supplied to the FormView's context.
        '''
        # Instantiate Form.

        form_class = super(CheckoutFormView, self).get_form_class()

        logger.debug('Getting a %s form' % (form_class.__name__,))
        form = form_class(**self.get_form_kwargs())

        if isinstance(form, AddressForm):
            # Determine the IP address associated to the HTTP Request.
            ip_address = get_real_ip(self.request)
    
            # Populate the form's `country` field with the user's apparent
            # location.
            if ip_address and not form.is_bound:
                geo_ip2 = GeoIP2()
                location = geo_ip2.country(ip_address)
                form.fields['country'].initial = location['country_code']

        logger.debug(
            'The %s form is %s' % (
                form_class.__name__, 'bound' if form.is_bound else 'unbound'
            )
        )

        return form


    def form_valid(self, form):

        if not self.request.session.has_key(UUID):
            self.request.session[UUID] = {}

        self.request.session[UUID].update({
            self.current_step['name']: form.cleaned_data,
        })
        self.request.session.modified = True

        return super(CheckoutFormView, self).form_valid(form)


    def get_success_url(self):
        logger.debug('Getting Success URL...')

        if self.get_current_step():
            url = reverse_lazy('checkout')
        else:
            url = self.success_url
            del self.request.session[UUID]

        logger.debug('Redirecting to %s' % url)

        return url


    def get_context_data(self, **kwargs):
        context = super(CheckoutFormView, self).get_context_data(**kwargs)

        current_position = next(
            i for (i, step) in enumerate(self.steps)
            if step['name'] == self.current_step['name']
        )

        context.update({
            'current_position': current_position,
            'total_steps': range(len(self.steps)),
        })

        step_context = self.current_step['context']
        if step_context:
            context.update(step_context)

        return context
