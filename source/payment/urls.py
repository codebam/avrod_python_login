from django.urls import path
from .views import LicenseView, PaymentSuccessView, ManageLicenseView, UpdateSubscriptionView

from . import views

app_name = 'payment'

urlpatterns = [
    path('', LicenseView.as_view(), name='licensing'),
    path('manage/<str:sub_id>/', ManageLicenseView.as_view(), name='manage'),
    path('manage/<str:sub_id>/success/', UpdateSubscriptionView.as_view(), name='updated'),
    path('success/', PaymentSuccessView.as_view(), name='checkout'),
    path('webhook/', views.webhook, name='webhook'),
]
