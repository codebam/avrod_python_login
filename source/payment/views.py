import stripe
import json
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateCustomerForm

class HomePageView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY

        return context

class CreateCustomerView(LoginRequiredMixin, FormView):
    template_name = 'create_customer.html'
    form_class = CreateCustomerForm

    def form_valid(self, form):
        customer = self.create_customer(self.request)
        create_customer_in_database(self, form, customer)

    
    def create_customer_in_database(self, form, customer):
        request = self.request
        user = self.request.user
        result = json.loads(request.body)
        customer = form.save(commit=False)
        customer.customer_id = result.id
        customer.user_id = user
        customer.save()

    def create_customer(request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            result = json.loads(request.body)

            return stripe.Customer.create(
                payment_method=result.payment_method,
                email=result.email,
                invoice_settings={
                        'default_payment_method': result.payment_method,
                    },
                )
