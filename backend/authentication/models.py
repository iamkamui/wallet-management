from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager): ...


class Profile(models.Model):
    cpf = models.CharField("cpf", max_length=11, blank=False, unique=True)  # TODO: Criar o validator do campo CPF
    email = models.EmailField("email", max_length=254, unique=True, null=False)
    preferred_name = models.CharField("preferred name", max_length=50, blank=False, null=False)
    full_name = models.CharField("full name", max_length=254, blank=False)
    phone_number = PhoneNumberField("phone number", blank=True)

    class Meta:
        abstract = True


class User(Profile, AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email", "preferred_name"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
