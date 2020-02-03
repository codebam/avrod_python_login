from django.db import models

class Session(models.Model):
    session_key = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class License(models.Model):
    license_key = models.CharField(max_length=32, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    license_key = models.ForeignKey(License, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


