from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages



@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'profile.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class CreateEmployeeView(View):
    def get(self, request):
        form = EmployeeCreationForm()
        employees = Employee.objects.all()
        occupations = Occupation.objects.all()
        return render(request, 'cadastroFuncionario.html', {'form': form, 'employees': employees, 'occupations': occupations})

    def post(self, request):
        form = EmployeeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Funcionário criado com sucesso!')
                return redirect('employee')  # Substitua pelo nome da sua URL de listagem
            except IntegrityError as e:
                messages.error(request, f'Erro ao criar funcionário: {e}')
        else:
            messages.error(request, 'Erro ao criar funcionário. Verifique os dados inseridos.')
        employees = Employee.objects.all()
        occupations = Occupation.objects.all()
        return render(request, 'cadastroFuncionario.html', {'form': form, 'employees': employees, 'occupations': occupations})

@method_decorator(login_required, name='dispatch')
class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.all()
        return render(request, 'funcionarios.html', {'employees': employees})