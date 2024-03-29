from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import activate, get_language, gettext_lazy as _

from allauth.account.signals import user_signed_up

from emails.tasks import send_mail
from countries.utils import get_country_from_language_code
from rowticket.fields import LanguageCodeField
from rowticket.frontend_urls import get_frontend_url
from rowticket.models import AbstractBaseModel

VAT_CONDITIONS = [
    ('responsable_inscripto', _('Responsable Inscripto')),
    ('monotributo', _('Monotributo')),
    ('consumidor_final', _('Consumidor Final')),
    ('exento', _('Exento'))
]

class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, password=None
    ):
        if not email:
            raise ValueError(_('El campo email es obligatorio'))

        if not first_name:
            raise ValueError(_('El campo nombre es obligatorio'))

        if not last_name:
            raise ValueError(_('El campo apellido es obligatorio'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email, first_name, last_name, password=None
    ):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('nombre'), max_length=100)
    last_name = models.CharField(_('apellido'), max_length=100)
    shipping_address = models.OneToOneField(
        'addresses.Address', blank=True, null=True, verbose_name=_('Dirección de facturación'),
        on_delete=models.SET_NULL, related_name='user_shipping_address'
    )
    billing_address = models.OneToOneField(
        'addresses.Address', blank=True, null=True, verbose_name=_('Dirección de envío'),
        on_delete=models.SET_NULL, related_name='user_billing_address'
    )

    is_staff = models.BooleanField(_('es staff'), default=False)
    is_active = models.BooleanField(_('activo'), default=True)
    language_code = LanguageCodeField(_('código de idioma'))
    vat_condition = models.CharField(_('condicion IVA'), choices=VAT_CONDITIONS, max_length=50, null=True, default='consumidor_final')
    bank_name = models.CharField(_('Banco'), max_length=100, null=True, default='')
    bank_type = models.CharField(_('tipo de cuenta'), max_length=100, null=True, default='')
    bank_number = models.CharField(_('cuenta bancaria'), max_length=100, null=True, default='')
    bank_cbu = models.CharField(_('cbu'), max_length=100, null=True, default='')
    bank_cuit = models.CharField(_('cuit'), max_length=100, null=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    get_full_name.short_description = _('nombre completo')
    get_full_name.admin_order_field = ('last_name', )

    def get_signup_country(self):
        return get_country_from_language_code(self.language_code)

    def get_short_name(self):
        return self.first_name

    def clean(self):
        if self.email:
            queryset = User.objects.all()

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            try:
                queryset.get(email__iexact=self.email)

                raise ValidationError({
                    'email': _('Ya existe un usuario con este email')
                })

            except User.DoesNotExist:
                pass

        self.email = self.email.lower()

        return super().clean()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')


# Signals
def on_user_signup(sender, request, user, **kwargs):
    context = {
        'user': user,
        'my_account_url': get_frontend_url('my_account', get_country_from_language_code(user.language_code))
    }

    current_language = get_language()

    activate(user.language_code)
    send_mail('signup', _('¡Se ha creado tu cuenta en ROW Ticket Argentina!'), context, user.email)
    activate(current_language)


user_signed_up.connect(on_user_signup)
