from django.db import models
from django.utils import timezone

# Create your models here.


class AppUser(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    profile_photo = models.CharField(max_length=256, null=True)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return self.user_id


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, primary_key=True)
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=100)
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Kyc_documents(models.Model):
    id_passport_front = models.CharField(max_length=200, null=True)
    id_passport_back = models.CharField(max_length=200, null=True)
    id_passport_number = models.BigIntegerField(null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
