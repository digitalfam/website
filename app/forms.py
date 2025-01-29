from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Senha')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'cpf', 'phone']


class EmployeeCreationForm(UserCreationForm):
    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Função')
    cpf = forms.CharField(max_length=14, required=True, label='CPF')
    phone = forms.CharField(max_length=15, required=False, label='Telefone')
    address = forms.CharField(max_length=200, required=True, label='Endereço')
    neighborhood = forms.CharField(max_length=100, required=True, label='Bairro')
    number = forms.CharField(max_length=10, required=True, label='Número')
    urban_or_rural = forms.ChoiceField(
        choices=[('Urbano', 'Urbano'), ('Rural', 'Rural')],
        required=True,
        label='Zona'
    )
    city = forms.CharField(max_length=100, required=True, label='Cidade')
    emergency_phone = forms.CharField(max_length=15, required=True, label='Telefone de Emergência')
    
    occupation = forms.ModelChoiceField(
        queryset=Occupation.objects.all(),
        required=False,
        label='Ocupação'
    )
    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Salário'
    )
    admission = forms.DateField(
        required=False,
        label='Data de Admissão',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    resignation = forms.DateField(
        required=False,
        label='Data de Demissão',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    photo = forms.ImageField(required=False, label='Foto')
    
    class Meta:
        model = User
        fields = (
            'username', 'password1', 'password2',
            'role', 'cpf', 'phone', 'address', 'neighborhood',
            'number', 'urban_or_rural', 'city', 'emergency_phone',
            'occupation', 'salary', 'admission', 'resignation', 'photo'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'urban_or_rural': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'admission': forms.DateInput(attrs={'class': 'form-control'}),
            'resignation': forms.DateInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            try:
                user.save()
            except IntegrityError:
                raise IntegrityError("Erro ao criar usuário. O CPF deve ser único.")
            
            # Atualizar o Profile existente criado pelo sinal
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.cpf = self.cleaned_data['cpf']
            profile.phone = self.cleaned_data['phone']
            profile.address = self.cleaned_data['address']
            profile.neighborhood = self.cleaned_data['neighborhood']
            profile.number = self.cleaned_data['number']
            profile.urban_or_rural = self.cleaned_data['urban_or_rural']
            profile.city = self.cleaned_data['city']
            profile.emergency_phone = self.cleaned_data['emergency_phone']
            profile.save()
            
            # Criar o Employee vinculado ao User existente
            try:
                Employee.objects.create(
                    user=user,
                    occupation=self.cleaned_data['occupation'],
                    salary=self.cleaned_data['salary'],
                    admission=self.cleaned_data['admission'],
                    resignation=self.cleaned_data['resignation'],
                    photo=self.cleaned_data['photo']
                )
            except IntegrityError:
                raise IntegrityError("Erro ao criar funcionário. O perfil já está vinculado a um funcionário.")
        
        return user