# Generated by Django 2.2.4 on 2020-03-20 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20200228_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='cardholder',
        ),
    ]
