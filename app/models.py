from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PAI', 'Pai'),
        ('FUNCIONARIO', 'Funcionário'),
        ('OUTRO', 'Outro'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OUTRO', verbose_name='Função')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    date = models.DateField(verbose_name='Data')
    time = models.TimeField(verbose_name='Hora')
    is_present = models.BooleanField(default=False, verbose_name='Presente')

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.time}'
    
    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    title = models.CharField(max_length=100, verbose_name='Título')
    file = models.FileField(upload_to='docs/', verbose_name='Arquivo') # Alterar lógica depois
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')

    def __str__(self):
        return f'{self.user.username} - {self.title}'
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    model_name = models.CharField(max_length=100, verbose_name='Modelo')
    object_id = models.PositiveIntegerField(verbose_name='ID do Objeto')
    action = models.CharField(max_length=50, verbose_name='Ação')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')

    def __str__(self):
        return f'{self.user.username} - {self.model_name} - {self.action}'
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'

