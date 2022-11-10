from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone as tz
from django.utils.translation import gettext_lazy as _

from cognitive.apps.organization.models import Organization

from .exceptions import SuperUserAlreadyExists


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given data.
        """
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        # We need to have only one superuser account (platform account)
        users = User.objects.filter(is_superuser=True)
        if users.exists():
            raise SuperUserAlreadyExists()
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrator')

        return self.create_user(email=self.normalize_email(email), password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    CLIENT = 'client'
    MANAGER = 'manager'
    ADMINISTRATOR = 'administrator'

    ROLE_CHOICES = (
        (CLIENT, 'Client'),
        (MANAGER, 'Manager'),
        (ADMINISTRATOR, 'Administrator')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=24, choices=ROLE_CHOICES, default='employee')
    email = models.EmailField(_('email address'), unique=True)
    organization = models.ManyToManyField(
        Organization, related_name='organization', blank=True)
    created_at = models.DateTimeField(default=tz.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
