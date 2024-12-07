from django.contrib import admin

# Register your models here.
from facturador.apps.company.models import PlanEmpresa, Empresa

admin.site.register(PlanEmpresa)

admin.site.register(Empresa)
