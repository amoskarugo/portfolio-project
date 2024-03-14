from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Account(models.Model):
    ACCOUNT_TYPE = [
        ('S', 'Saving'),
        ('C', 'Checking')
    ]
    account_id = models.BigIntegerField(primary_key=True)
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, null=False, choices=ACCOUNT_TYPE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('CA', 'Canceled'),
        ('P', 'Pending'),
        ('CO', 'Completed'),
    ]
    DESCRIPTION = [
        ('T', 'Transfer'),
        ('D' ,'Deposit'),
        ('W', 'Withdraw')
    ]
    transaction_id = models.BigIntegerField(primary_key=True)
    from_account = models.BigIntegerField(null=False)
    to_account = models.BigIntegerField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.CharField(null=False, max_length=100, choices=DESCRIPTION)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=False, max_length=2, choices=STATUS_CHOICES)
