from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True, label="Mobile Number")
    account_type = forms.ChoiceField(choices=Profile.ACCOUNT_TYPES, initial='savings')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'account_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.phone = self.cleaned_data['phone']
            user.profile.account_type = self.cleaned_data['account_type']
            user.profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']
