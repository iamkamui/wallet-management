from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from authentication.validators import CPFValidator


class Profile(models.Model):
    user = models.OneToOneField("User", verbose_name="User", related_name="profile", on_delete=models.CASCADE)
    preferred_name = models.CharField("preferred name", max_length=50, blank=False, default="")
    full_name = models.CharField("full name", max_length=254, blank=False, default="")
    phone_number = PhoneNumberField("phone number", blank=True)


class UserManager(BaseUserManager["User"]):  # type: ignore
    def _create_user_object(self, cpf: str, email: str, password: str, **extra_fields: Any) -> "User":
        is_admin = extra_fields.get("admin")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email)
        user.password = make_password(password)

        if is_admin:
            user.is_staff = True

        user.full_clean()
        user.save(using=self._db)

        user.refresh_from_db()
        return user

    def create_user(self, cpf: str, email: str, password: str, **extra_fields: Any) -> "User":  # type: ignore
        if not email:
            raise ValueError("You must have set an email address.")

        if not cpf:
            raise ValueError("You must have an valid CPF number.")

        return self._create_user_object(cpf, email, password, **extra_fields)

    def create_superuser(self, cpf: str, email: str, password: str, admin: bool = True, **extra_fields: Any) -> "User":  # type: ignore
        return self._create_user_object(cpf, email, password, admin=admin, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField("cpf", max_length=11, validators=[CPFValidator()], blank=False, unique=True)
    email = models.EmailField("email", max_length=254, unique=True, null=False)
    is_staff = models.BooleanField("staff status", default=False)
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def is_active(self) -> bool:  # type: ignore
        if not self.profile:
            return False
        return bool(self.profile.preferred_name and self.profile.full_name)
