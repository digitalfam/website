from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Profile(models.Model):
    ROLE_CHOICES = (
        ('RESPONSAVEL', 'Responsável'),
        ('FUNCIONARIO', 'Funcionário'),
        ('OUTRO', 'Outro'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OUTRO', verbose_name='Função')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF')
    phone = models.CharField(max_length=15, blank=True, null=True, default='00 0 0000-0000', verbose_name='Telefone')
    address = models.CharField(max_length=200, default='Default Address', verbose_name='Endereço')
    neighborhood = models.CharField(max_length=100, default='Centro', verbose_name='Bairro')
    number = models.CharField(max_length=10, default='000', verbose_name='Número')
    urban_or_rural = models.CharField(
        max_length=10,
        choices=[('Urbano', 'Urbano'), ('Rural', 'Rural')],
        default='Urbano',
        verbose_name='Zona'
    )
    city = models.CharField(max_length=100, default='Muzambinho-MG', verbose_name='Cidade')
    emergency_phone = models.CharField(max_length=15, default='00 0 0000-0000', verbose_name='Telefone de Emergência')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['user__username']

class Occupation(models.Model):
    name = models.CharField(max_length=100, default='Ocupação Padrão', verbose_name='Nome da Ocupação')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ocupação'
        verbose_name_plural = 'Ocupações'
        ordering = ['name']

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Ocupação')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00, verbose_name='Salário')
    admission = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Data de Admissão')
    resignation = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Data de Demissão')
    photo = models.ImageField(upload_to='fotos/funcionarios/', blank=True, null=True, verbose_name='Foto')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['user__username']

class DocumentEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Funcionário')
    title = models.CharField(max_length=100, default='Título Padrão', verbose_name='Título')
    file = models.FileField(upload_to='docs/funcionarios/', verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Envio')

    def __str__(self):
        return f'{self.employee.user.username} - {self.title}'

    class Meta:
        verbose_name = 'Documento do Funcionário'
        verbose_name_plural = 'Documentos dos Funcionários'
        ordering = ['-uploaded_at']

class Students(models.Model):
    name = models.CharField(max_length=100, default='Nome Padrão', verbose_name='Nome')
    last_name = models.CharField(max_length=100, default='Sobrenome Padrão', verbose_name='Sobrenome')
    birth_date = models.DateField(default=timezone.now, verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    mother_name = models.CharField(max_length=100, default='Nome da Mãe Padrão', verbose_name='Nome da Mãe')
    father_name = models.CharField(max_length=100, default='Nome do Pai Padrão', verbose_name='Nome do Pai')
    address = models.CharField(max_length=200, default='Endereço Padrão', verbose_name='Endereço')
    neighborhood = models.CharField(max_length=100, default='Centro', verbose_name='Bairro')
    number = models.CharField(max_length=10, default='000', verbose_name='Número')
    urban_or_rural = models.CharField(max_length=10, choices=[('Urbano', 'Urbano'), ('Rural', 'Rural')], default='Urbano', verbose_name='Zona')
    city = models.CharField(max_length=100, default='Muzambinho-MG', verbose_name='Cidade')
    emergency_phone = models.CharField(max_length=15, default='00 0 0000-0000', verbose_name='Telefone de Emergência')
    photo = models.ImageField(upload_to='fotos/estudantes/', verbose_name='Foto')
    enrollment_number = models.CharField(max_length=20, unique=True, verbose_name='Número de Matrícula')
    observations = models.TextField(blank=True, null=True, verbose_name='Observações')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')

    def __str__(self):
        return f'{self.name} {self.last_name}'

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
        ordering = ['name', 'last_name']

class DocumentStudent(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Aluno')
    title = models.CharField(max_length=100, default='Título Padrão', verbose_name='Título')
    file = models.FileField(upload_to='docs/estudantes/', verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Envio')

    def __str__(self):
        return f'{self.student.name} {self.student.last_name} - {self.title}'

    class Meta:
        verbose_name = 'Documento do Estudante'
        verbose_name_plural = 'Documentos dos Estudantes'
        ordering = ['-uploaded_at']

class Class(models.Model):
    name = models.CharField(max_length=100, default='Nome da Turma Padrão', verbose_name='Nome')
    students = models.ManyToManyField(Students, verbose_name='Estudantes', related_name='classes')
    teacher = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Professor')
    shift = models.CharField(max_length=20, choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')], verbose_name='Turno')
    image = models.ImageField(upload_to='fotos/turmas/', verbose_name='Foto')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['name']

class AttendanceStudents(models.Model):
    turma = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendances', verbose_name='Turma')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='attendances', verbose_name='Aluno')
    date = models.DateField(verbose_name='Data')
    present = models.BooleanField(default=False, verbose_name='Presente')
    notes = models.TextField(blank=True, null=True, default='Sem observações', verbose_name='Observações')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')

    def __str__(self):
        status = 'Presente' if self.present else 'Ausente'
        return f'{self.student.name} {self.student.last_name} - {self.turma.name} - {self.date} - {status}'

    class Meta:
        verbose_name = 'Registro de Frequência'
        verbose_name_plural = 'Registros de Frequência'
        unique_together = ('turma', 'student', 'date')
        ordering = ['-date']

class Parents(Profile):
    son = models.ManyToManyField(Students, verbose_name='Filhos', related_name='parents')
    photo = models.ImageField(upload_to='pais/', verbose_name='Foto')
   

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Pai/Mãe'
        verbose_name_plural = 'Pais/Mães'
        ordering = ['user__username']

class DocumentParent(models.Model):
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, verbose_name='Pai/Mãe')
    title = models.CharField(max_length=100, default='Título Padrão', verbose_name='Título')
    file = models.FileField(upload_to='docs/pais/', verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Envio')

    def __str__(self):
        return f'{self.parent.user.username} - {self.title}'

    class Meta:
        verbose_name = 'Documento do Pai/Mãe'
        verbose_name_plural = 'Documentos dos Pais/Mães'
        ordering = ['-uploaded_at']
        
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    model_name = models.CharField(max_length=100, default='Modelo Padrão', verbose_name='Modelo')
    object_id = models.PositiveIntegerField(verbose_name='ID do Objeto')
    action = models.CharField(max_length=50, default='Ação Padrão', verbose_name='Ação')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Data/Hora')

    def __str__(self):
        return f'{self.user.username} - {self.model_name} - {self.action}'

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']