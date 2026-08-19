from django.contrib import admin
from .models import Transaction, ChatLog


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('txn_id', 'sender', 'receiver', 'amount', 'status', 'timestamp')
    search_fields = ('txn_id', 'sender__user__username', 'receiver__user__username')
    list_filter = ('status', 'txn_type')


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
