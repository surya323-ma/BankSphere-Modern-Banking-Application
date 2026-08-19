from decimal import Decimal

from django import forms

from accounts.models import Profile


class TransferForm(forms.Form):
    recipient = forms.CharField(
        label="Recipient Account Number / Username",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter account number or username', 'autocomplete': 'off'})
    )
    amount = forms.DecimalField(
        label="Amount (₹)", max_digits=14, decimal_places=2, min_value=Decimal('1.00'),
        widget=forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'})
    )
    note = forms.CharField(label="Note (optional)", max_length=140, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'e.g. Rent, dinner, gift'}))

    def clean_recipient(self):
        value = self.cleaned_data['recipient'].strip()
        profile = Profile.objects.filter(account_number=value).first() or \
            Profile.objects.filter(user__username__iexact=value).first()
        if not profile:
            raise forms.ValidationError("No BankSwift account found with this account number or username.")
        self.cleaned_profile = profile
        return value
