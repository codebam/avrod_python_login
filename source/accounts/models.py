from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class License(models.Model):
    key = models.CharField(max_length=20, unique=True)
    expiry = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.PROTECT)
