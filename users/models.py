from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone_number, pin, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(pin)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)  # Auto increment integer ID
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID reference
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID reference
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # CREDIT or DEBIT
    remarks = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class TopUp(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID reference
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_top_up = models.DecimalField(max_digits=10, decimal_places=2)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID sebagai reference
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=255)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)


class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID sebagai reference
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transfer_sender')
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transfer_receiver')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=255)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

