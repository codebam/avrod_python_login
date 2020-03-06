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
    cardholder = models.CharField(max_length=100)

    @classmethod
    def create(cls, customer_id, user_id, cardholder):
        customer = cls(customer_id=customer_id, user_id=user_id, cardholder=cardholder)
        return customer


class Subscription(models.Model):
    sub_id = models.CharField(max_length=18, unique=True, primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    license_key = models.CharField(max_length=20) # license_key = models.ForeignKey(License, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, sub_id, customer_id, license_key, created_at):
        subscription = cls(sub_id=sub_id, customer_id=customer_id, license_key=license_key, created_at=created_at)
        return subscription
