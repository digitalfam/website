#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")# Substitua 'seu_projeto' pelo nome do seu projeto
django.setup()

from django.utils import timezone
from app.models import Students

# Loop para criar 28 estudantes
for i in range(1, 29):
    student = Students.objects.create(
        name=f"Aluno {i}",
        last_name=f"Sobrenome {i}",
        birth_date="2000-01-01",  # Data de nascimento fixa para exemplo
        cpf=f"000.000.000-{i:02d}",  # Exemplo: 000.000.000-01, 000.000.000-02, etc.
        mother_name=f"Mãe do Aluno {i}",
        father_name=f"Pai do Aluno {i}",
        address=f"Rua Exemplo, {i}",
        neighborhood=f"Bairro {i}",
        number=str(i),
        urban_or_rural="Urbano",
        city="Muzambinho-MG",
        emergency_phone="123456789",  # Número de emergência fictício
        photo="fotos/estudantes/default.jpg",  # Utilize uma imagem padrão existente
        enrollment_number=f"MAT{i:04d}",
        observations="",
        created_at=timezone.now()
    )
    print(f"Cadastrado: {student}")