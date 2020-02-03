from django.forms import ModelForm
from payment.models import Customer

class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('customer_id', 'user_id')
