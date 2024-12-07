import uuid

from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from stdimage import StdImageField

phone_regex = RegexValidator(regex=r'^\d{8,14}((,\d{8,14})?)*$',
                             message="El formato del teléfono debe ser: '9998888777', sin código de país. De 8-14 "
                                       "dígitos permitidos. Puede agregar más telefonos seperados por coma.")

# Create your models here.
class TipoUsuario(models.Model):
    name = models.CharField('Nombre', max_length=20)

    def __str__(self):
        return self.name


class TipoPersona(models.Model):
    name = models.CharField('Nombre', max_length=20)

    def __str__(self):
        return self.name


class ClientStatus(models.Model):
    name = models.CharField(max_length=70, verbose_name='Nombre')
    class_css = models.CharField(max_length=40, verbose_name="Class ccs color")
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Estado Clientes"
        verbose_name_plural = "Estado Clientes"

    def __str__(self):
        return self.name


class User(AbstractUser):
    numero_regex = RegexValidator(regex=r'^\d+$', message='Ingrese solo números.')

    ADMIN = 'Admin'
    TECNICO = 'Tecnico'
    SOPORTE = 'Soporte'
    VENTAS = 'Ventas'
    CLIENTE = 'Cliente'
    PROSPECTO = 'Prospecto'
    TYPE = (
        (ADMIN, 'Administrador'),
        (TECNICO, 'Técnico'),
        (SOPORTE, 'Soporte'),
        (VENTAS, 'Ventas'),
        (CLIENTE, 'Cliente'),
        (PROSPECTO, 'Prospecto'),
    )

    MORAL = 'Moral/Juridica'
    FISICA = 'Fisica/Natural'
    TIPO_PERSONA = (
        (FISICA, 'Fisica/Natural'),
        (MORAL, 'Moral/Juridica')
    )

    def avatar_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "usuarios/{}/avatar/{}.{}".format(
            connection.tenant.domain_url, slugify(str(file_name)), extension
        )
        return url

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    avatar = StdImageField('Avatar', upload_to='usuarios/%Y/%m/', default='usuarios/avatar.png',
                           variations={
                               'perfil': {'width': 240, 'height': 240, 'crop': True},
                               'thumbnail': {'width': 45, 'height': 45, 'crop': True}
                           })
    address = models.TextField("Dirección", blank=True)
    phone_number = models.CharField("Teléfono Celular", max_length=250, blank=True,
                                    validators=[phone_regex])
    rfc = models.CharField('RFC/RUC/NIT', max_length=30, blank=True)
    legal_name = models.CharField('Nombre facturación', max_length=255, blank=True)
    tax_id = models.CharField('RFC/RUC', max_length=30, blank=True)
    tax_system = models.CharField('Regimen fiscal', max_length=10, blank=True, null=True)
    postal_code = models.CharField('Código postal', max_length=50, blank=True)
    billing_address = models.TextField('Dirección de facturación', max_length=100, blank=True)
    billing_email = models.EmailField('Email de facturación', blank=True)
    district = models.CharField('Localidad/Barrio/Departamento', max_length=50, blank=True)
    city = models.CharField('Ciudad/Municipio', max_length=50, blank=True)
    license = models.CharField('Licencia DNI/C.I./C.C.', max_length=35, blank=True)
    
    # relations
    user_type = models.ForeignKey(TipoUsuario, verbose_name='Tipo de usuario', null=True,
                                  related_name='user_type_user', on_delete=models.SET_NULL)
    person_type = models.ForeignKey(TipoPersona, verbose_name='Tipo de persona', blank=True, null=True,
                                    related_name='person_type_user', on_delete=models.SET_NULL)

    status = models.ForeignKey(ClientStatus, related_name="client_status", verbose_name="Estatus",
                               on_delete=models.SET_NULL, null=True, blank=True)

    company = models.ForeignKey('company.Empresa', verbose_name='Empresa', null=True, related_name='company_user',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '-' + self.get_full_name()

    class Meta:
        ordering = ('-id',)


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    class Meta:
        unique_together = ('user', 'role')


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

    class Meta:
        unique_together = ('role', 'permission')