# Generated by Django 2.2.4 on 2020-03-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_subscription_renewal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='renewal_date',
            field=models.DateField(),
        ),
    ]
