#!/bin/bash
# Esperar a que la base de datos esté lista
wait-for-it db:3306

# Ejecutar las migraciones
python manage.py migrate

# Crear el superusuario con contraseña
python manage.py shell <<EOF
from facturador.apps.users.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
EOF

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000
