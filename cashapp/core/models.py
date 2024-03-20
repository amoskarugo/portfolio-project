# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


# Create your CustomUserManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)


# Create your User Model here.
class User(AbstractUser, PermissionsMixin):
    # AbstractBaseUser has password, last_login, is_active by default

    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=250)

    is_staff = models.BooleanField(default=True)  # must be needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)  # must be needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False)  # this field we inherit from PermissionsMixin.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Account(models.Model):
    ACCOUNT_TYPE = [
        ('S', 'Saving'),
        ('C', 'Checking')
    ]
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, null=False, choices=ACCOUNT_TYPE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('CA', 'Canceled'),
        ('P', 'Pending'),
        ('CO', 'Completed'),
    ]
    DESCRIPTION = [
        ('T', 'Transfer'),
        ('BD', 'Bank Deposit'),
        ('BW', 'Withdraw to Bank'),
        ('WM', 'Withdraw to mobile wallet'),
        ('MD', 'Merchant Deposit'),
        ('MW', 'Merchant withdraw'),
        ('MD', 'Mobile wallet deposit')
    ]
    transaction_id = models.CharField(primary_key=True, max_length=255)
    from_account = models.BigIntegerField(null=False, default=0)
    to_account = models.BigIntegerField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.CharField(null=False, max_length=100, choices=DESCRIPTION)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=False, max_length=2, choices=STATUS_CHOICES)
