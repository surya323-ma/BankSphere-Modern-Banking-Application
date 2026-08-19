import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models


class Transaction(models.Model):
    TXN_TYPES = [
        ('transfer', 'Money Transfer'),
        ('deposit', 'Self Deposit'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    txn_id = models.CharField(max_length=20, unique=True, editable=False)
    sender = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    receiver = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    txn_type = models.CharField(max_length=10, choices=TXN_TYPES, default='transfer')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='success')
    note = models.CharField(max_length=140, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if not self.txn_id:
            self.txn_id = 'BST' + uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.txn_id} - {self.amount}"


class ChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_logs', null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
