from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models, transaction
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField("User", verbose_name="User", related_name="profile", on_delete=models.CASCADE)
    preferred_name = models.CharField("preferred name", max_length=50, blank=False, default="")
    full_name = models.CharField("full name", max_length=254, blank=False, default="")
    phone_number = PhoneNumberField("phone number", blank=True)


class UserManager(BaseUserManager):
    @transaction.atomic
    def _create_user(self, cpf: str, email: str, password: str, **extra_fields):
        if extra_fields.get("admin"):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        Profile.objects.create(user)
        return user

    def create_user(self, cpf: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("You must have set an email address.")

        if not cpf:
            raise ValueError("You must have an valid CPF number.")

        return self._create_user(cpf, email, password, **extra_fields)

    def create_superuser(self, cpf: str, email: str, password: str, admin=True, **extra_fields):
        return self._create_user(cpf, email, password, admin, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField("cpf", max_length=11, blank=False, unique=True)  # TODO: Criar o validator do campo CPF
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
    def is_active(self) -> bool:
        if not self.profile:
            return False
        return self.profile.preferred_name and self.profile.full_name
