from django.urls import path, include

from authentication.views import steam_auth_view

app_name='authentication'

urlpatterns = [
    path('steam/', steam_auth_view, name='steam')
]