from django.db import models

class Subscription(models.Model):
    license_key = models.ForeignKey(License, on_delete=models.SET_NULL)
    session_key = models.ForeignKey(Session, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class Session(models.Model):
    session_key = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class License(models.Model):
    license_key = models.CharField(max_length=32, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
