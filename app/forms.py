from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Senha')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'cpf', 'phone']
