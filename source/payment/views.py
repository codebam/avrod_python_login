import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def process(request):
    if request.method == 'POST':
        process = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django process',
            source=request.POST['stripeToken']
        )
        return render(request, 'process.html')

