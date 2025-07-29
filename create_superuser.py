#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Criar superusuário se não existir
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('Superusuário "admin" criado com sucesso!')
    print('Username: admin')
    print('Password: admin123')
else:
    print('Superusuário "admin" já existe!')
