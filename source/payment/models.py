from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    session_key = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class License(models.Model):
    license_key = models.CharField(max_length=32, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    customer_id = models.CharField(max_length=18, unique=True, primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Subscription(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    license_key = models.ForeignKey(License, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
