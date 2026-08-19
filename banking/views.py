import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction as db_transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from .chatbot import get_bot_response
from .forms import TransferForm
from .models import Transaction, ChatLog


@login_required
def dashboard_view(request):
    profile = request.user.profile
    recent_txns = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).select_related('sender__user', 'receiver__user')[:6]

    total_in = sum(t.amount for t in recent_txns if t.receiver_id == profile.id)
    total_out = sum(t.amount for t in recent_txns if t.sender_id == profile.id)

    context = {
        'profile': profile,
        'recent_txns': recent_txns,
        'total_in': total_in,
        'total_out': total_out,
    }
    return render(request, 'banking/dashboard.html', context)


@login_required
def transfer_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_profile = form.cleaned_profile
            amount = form.cleaned_data['amount']
            note = form.cleaned_data['note']

            if recipient_profile.id == profile.id:
                messages.error(request, "You cannot transfer money to your own account.")
                return render(request, 'banking/transfer.html', {'form': form, 'profile': profile})

            try:
                with db_transaction.atomic():
                    sender_locked = Profile.objects.select_for_update().get(id=profile.id)
                    if sender_locked.balance < amount:
                        Transaction.objects.create(
                            sender=sender_locked, receiver=recipient_profile,
                            amount=amount, status='failed', note=note or 'Insufficient balance'
                        )
                        messages.error(request, "Transfer failed: insufficient balance.")
                        return render(request, 'banking/transfer.html', {'form': form, 'profile': profile})

                    receiver_locked = Profile.objects.select_for_update().get(id=recipient_profile.id)
                    sender_locked.balance -= amount
                    receiver_locked.balance += amount
                    sender_locked.save()
                    receiver_locked.save()

                    txn = Transaction.objects.create(
                        sender=sender_locked, receiver=receiver_locked,
                        amount=amount, status='success', note=note
                    )
                messages.success(request, f"₹{amount:,.2f} sent successfully to {recipient_profile.user.username}. Reference: {txn.txn_id}")
                return redirect('transaction_detail', txn_id=txn.txn_id)
            except Exception as e:
                messages.error(request, f"Transfer could not be completed: {e}")
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form, 'profile': profile})


@login_required
def transactions_view(request):
    profile = request.user.profile
    txn_qs = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).select_related('sender__user', 'receiver__user')

    txn_type = request.GET.get('type')
    if txn_type == 'sent':
        txn_qs = txn_qs.filter(sender=profile)
    elif txn_type == 'received':
        txn_qs = txn_qs.filter(receiver=profile)

    paginator = Paginator(txn_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'banking/transactions.html', {
        'profile': profile, 'page_obj': page_obj, 'txn_type': txn_type or 'all'
    })


@login_required
def transaction_detail_view(request, txn_id):
    profile = request.user.profile
    txn = get_object_or_404(
        Transaction.objects.filter(Q(sender=profile) | Q(receiver=profile)),
        txn_id=txn_id
    )
    return render(request, 'banking/transaction_detail.html', {'txn': txn, 'profile': profile})


@login_required
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    profile = request.user.profile
    response = get_bot_response(message, profile=profile)
    ChatLog.objects.create(user=request.user, message=message, response=response)
    return JsonResponse({'response': response})
