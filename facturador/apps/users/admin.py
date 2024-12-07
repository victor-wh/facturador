# django packages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# local packages
from facturador.apps.users.models import (
    User, TipoUsuario, TipoPersona, ClientStatus, Permission, Role, UserRole, RolePermission)


# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(TipoUsuario)

admin.site.register(TipoPersona)

admin.site.register(ClientStatus)

admin.site.register(Permission)

admin.site.register(Role)

admin.site.register(UserRole)

admin.site.register(RolePermission)
