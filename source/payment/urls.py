from django.urls import path
from .views import LicenseView, PaymentSuccessView, ManageLicenseView

from . import views

app_name = 'payment'

urlpatterns = [
    path('', LicenseView.as_view(), name='licensing'),
    path('manage/', ManageLicenseView.as_view(), name='manage'),
    path('success/', PaymentSuccessView.as_view(), name='checkout'),
    path('webhook/', views.webhook, name='webhook'),
]
