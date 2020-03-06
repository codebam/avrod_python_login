import stripe
import json
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Subscription, License

stripe.api_key = settings.STRIPE_SECRET_KEY

class LicenseView(LoginRequiredMixin, TemplateView):
    template_name = 'license.html'

    def get(self, request):
        user = self.request.user
        print(user)

        customer = Customer.objects.filter(user_id=user)
        print(customer)

        if customer.exists():
            print("customer exists")
            session = stripe.checkout.Session.create(
                customer = customer,
                payment_method_types=['card'],
                subscription_data={
                    'items': [{
                        'plan': 'plan_GfW2im5hu5EkF1',
                    }],
                },
                success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/licensing/',
            )
        else:
            print("customer does not exist")
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                subscription_data={
                    'items': [{
                        'plan': 'plan_GfW2im5hu5EkF1',
                    }],
                },
                success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/licensing/',
            )

        context = {
            'session_id': session.id
        }

        return render(request, self.template_name, context)


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'
        
