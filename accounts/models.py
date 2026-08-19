import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def generate_account_number():
    while True:
        number = str(random.randint(10**13, 10**14 - 1))  # 14 digit, Kotak-style
        if not Profile.objects.filter(account_number=number).exists():
            return number


class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_number = models.CharField(max_length=20, unique=True, editable=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='savings')
    phone = models.CharField(max_length=15, blank=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('5000.00'))
    ifsc = models.CharField(max_length=11, default='KKBK0000811')
    upi_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()
        if not self.upi_id:
            self.upi_id = f"{self.user.username}@bankswift"
        super().save(*args, **kwargs)

    def masked_account_number(self):
        return "XXXX XXXX " + self.account_number[-4:]

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
