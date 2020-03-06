from django.urls import path
from .views import LicenseView, PaymentSuccessView

from . import views

app_name = 'payment'

urlpatterns = [
    path('', LicenseView.as_view(), name='licensing'),
    path('success/', PaymentSuccessView.as_view(), name='checkout'),
]
