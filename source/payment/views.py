import stripe
import json
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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

    def get(self, request):
        print(request.session)
        print(request.session.get('stripe_customer'))

        return render(request, self.template_name)

        

endpoint_secret = ''

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("checkout.session.completed")

    if event['type'] == 'customer.created':
        stripe_customer = event['data']['object']
        print("customer.created")

    if event['type'] == 'customer.subscription.created':
        stripe_subscription = event['data']['object']
        print('customer.subscription.created')

    if event['type'] == 'charge.succeeded':
        charge = event['data']['object']
        print('charge.succeeded')

    return HttpResponse(status=200)
