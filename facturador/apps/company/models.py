import uuid as _uuid

from django.conf import settings
from django.core.validators import RegexValidator

from django.db import models

from stdimage import StdImageField
from django_countries.fields import CountryField

phone_regex = RegexValidator(regex=r'^\d{8,14}((,\d{8,14})?)*$',
                             message="El formato del teléfono debe ser: '9998888777', sin código de país. De 8-14 "
                                       "dígitos permitidos. Puede agregar más telefonos seperados por coma.")


# Create your models here.
class PlanEmpresa(models.Model):
    uuid = models.UUIDField(default=_uuid.uuid4, editable=False, db_index=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_sin_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mostrar = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        ordering = ('-created',)
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return '{}'.format(self.nombre)


class Empresa(models.Model):

    def logo_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "empresas/{}/logo/{}.{}".format(
            self.schema_name, slugify(str(file_name)), extension
        )
        return url

    ACTIVO = 1
    SUSPENDIDO = 2
    CANCELADO = 3
    ESTADO_EMPRESA = (
        (ACTIVO, 'Activo'),
        (SUSPENDIDO, 'Suspendido'),
        (CANCELADO, 'Cancelado'),
    )
    uuid = models.UUIDField(verbose_name='Identificador de empresa', editable=False, default=_uuid.uuid4,
                            db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    nombre = models.CharField(max_length=80, unique=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(max_length=100, blank=True)
    telefono = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    pais = CountryField()
    detalles = models.TextField(verbose_name="Detalles", blank=True)
    logo = StdImageField(upload_to=logo_path, default="empresas/logo-blanco.png",
                         variations={'thumbnail': {"width": 180, "height": 50, "crop": False}})
    estado = models.PositiveSmallIntegerField(choices=ESTADO_EMPRESA, default=ACTIVO, blank=True)
    is_active = models.BooleanField(default=True)
    
    fecha_contratacion = models.DateTimeField(blank=True, null=True)
    fecha_suspension = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Suspension")
    
    nombre_facturacion = models.CharField(max_length=255, blank=True)
    rfc = models.CharField(max_length=30, blank=True, verbose_name="RFC/RUC")
    regimen_fiscal = models.CharField(max_length=10, blank=True, null=True)
    codigo_postal = models.CharField(max_length=50, blank=True)
    direccion_facturacion = models.TextField(max_length=100, blank=True)
    email_facturacion = models.EmailField(blank=True)
    
    timezone = models.CharField(max_length=190, blank=False, null=False, default="Etc/UTC")
    # Grupos de Servidores y Subdominios
    external_id = models.PositiveIntegerField('Id externo del lote al que pertenece', db_index=True, blank=True,
                                              null=True)
    lote = models.CharField('Lote al que pertenece', max_length=50, default=settings.LOTE_PRINCIPAL)

    plan = models.ForeignKey(PlanEmpresa, related_name="empresa_plan_empresa", on_delete=models.SET_NULL,
                             null=True, blank=True,)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        permissions = {
            ('lista_empresas', 'Lista de empresas'),
            ('acciones_lista_empresas', 'Acciones lista de empresas'),
            ('crear_superusuarios', 'Crear super usuarios'),
            ('eliminar_superusuarios', 'Eliminar super usuarios'),
            ('ver_perfil_financiero', 'Ver perfil financiero'),
        }

    def __str__(self):
        return F"{self.nombre}"
