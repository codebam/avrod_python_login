from django.urls import path
from .views import CreateCustomerView

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('checkout/', CreateCustomerView.as_view(), name='checkout'),
]
