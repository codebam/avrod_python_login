from django.shortcuts import render
from django.http import HttpResponse


def steam_auth_view(request):
    return render(request, "authentication/steam.html", {})
