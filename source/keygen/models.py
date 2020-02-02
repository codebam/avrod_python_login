from django.db import models

class LicenseKey(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
