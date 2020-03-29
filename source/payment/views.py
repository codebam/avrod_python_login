import stripe
import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Subscription, License
from django.contrib.auth.models import User
from .keygen import generate
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY
global stripe_customer

class LicenseView(LoginRequiredMixin, TemplateView):
    template_name = 'license.html'

    def get(self, request):
        user = self.request.user
        customer = Customer.objects.filter(user_id=user)

        if customer.exists():
            customer_id = Customer.objects.values_list('customer_id', flat=True).get(user_id=user)
            subscription = Subscription.objects.filter(customer_id=customer_id)
            if subscription.exists():
                subscription = Subscription.objects.get(customer_id=customer_id)
                return redirect('payment:manage', sub_id=subscription.sub_id)
            else:
                session = stripe.checkout.Session.create(
                    customer = customer_id,
                    payment_method_types=['card'],
                    subscription_data={
                        'items': [{
                            'plan': 'plan_GfW2im5hu5EkF1',
                        }],
                    },
                    success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url='http://127.0.0.1:8000/licensing/',
                    metadata= {
                        'avrod_id': user.id
                    }
                )

        else:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                subscription_data={
                    'items': [{
                        'plan': 'plan_GfW2im5hu5EkF1',
                    }],
                },
                success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/licensing/',
                metadata= {
                    'avrod_id': user.id
                }
            )

        context = {
            'session_id': session.id
        }

        return render(request, self.template_name, context)
        

# Webhook Receiver
endpoint_secret = 'whsec_P2OxXQZFSLJ1F5kgPULOEKa0DcoqjVJj'
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

        user = User.objects.get(id = session.metadata.avrod_id)
        print(user)

        customer = Customer.objects.filter(user_id=user)
        print(customer)
        customer_id = session.customer
        if not customer.exists():
            # Create customer in Django
            customer = Customer.create(
                customer_id,
                user
            )
            customer.save()
        else:
            customer = Customer.objects.get(user_id=user)
        
        key = generate(get_random_string(32))
        license_key = License.create(key)
        license_key.save()
        stripe_sub = stripe.Subscription.retrieve(session.subscription)
        sub_end_date = datetime.datetime.utcfromtimestamp(float(stripe_sub.current_period_end))
        print(stripe_sub.id)
        print(sub_end_date)

        subscription = Subscription.create(
            stripe_sub.id,
            customer,
            license_key,
            sub_end_date
        )
        subscription.save()

    return HttpResponse(status=200)


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)


class ManageLicenseView(LoginRequiredMixin, TemplateView):
    template_name = 'manage.html'

    def get(self, request):
        return render(request, self.template_name)