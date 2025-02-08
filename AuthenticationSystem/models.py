from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
    Group,
    Permission,
)
import re
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
import random, string
from .services.sms_service import send_temporary_code


# Custom manager for CustomUser model
class CustomUserManeger(BaseUserManager):
    def create_customer(
        self,
        first_name=None,
        last_name=None,
        phone_number=None,
        user_type="customer",
        email=None,
        password=None,
        username=None,
        active_mode=True,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not username:
            raise ValueError("The 'username' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")

        if self.model.objects.filter(username=username).exists():
            raise ValueError(f"The 'username' {username} is already taken.")

        if email:
            email = self.normalize_email(email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            email=email,
            username=username,
            active_mode=active_mode,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_store_owner(
        self,
        first_name=None,
        last_name=None,
        phone_number=None,
        user_type="store_owner",
        email=None,
        password=None,
        username=None,
        store_location=None,
        national_code=None,
        store_name=None,
        store_logo=None,
        active_mode=True,
        store_industry=None,
        store_description=None,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not username:
            raise ValueError("The 'username' must be set")
        elif not store_name:
            raise ValueError("The 'store_name' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")
        elif not store_industry:
            raise ValueError("The 'store_industry' must be set")

        if self.model.objects.filter(username=username).exists():
            raise ValueError(f"The 'username' {username} is already taken.")

        if email:
            email = self.normalize_email(email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            email=email,
            national_code=national_code,
            store_location=store_location,
            store_logo=store_logo,
            username=username,
            active_mode=active_mode,
            store_industry=store_industry,
            store_description=store_description,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self,
        first_name=None,
        last_name=None,
        phone_number=None,
        user_type="admin",
        username=None,
        email=None,
        national_code=None,
        active_mode=True,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not username:
            raise ValueError("The 'username' must be set")
        elif not phone_number:
            raise ValueError("The 'phone_number' must be set")

        if self.model.objects.filter(username=username).exists():
            raise ValueError(f"The 'username' {username} is already taken.")

        temporary_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            username=username,
            active_mode=active_mode,
            **extra_fields,
        )

        user.set_password(temporary_password)
        send_temporary_code(phone_number=phone_number, code=temporary_password)
        user.save(using=self._db)
        return user


# Store Industry Model
class Store_Industry(models.Model):
    store_industry = models.CharField(max_length=50)

    def __str__(self):
        return self.store_industry


# Validator for file size
def validate_file_size(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size must be under {max_size_mb}MB.")


# Validator for phone number (Example for Iran phone numbers)
phone_number_validator = RegexValidator(
    regex=r"^\+98[0-9]{9}$",  # Example pattern for Iranian phone numbers: +98xxxxxxxxx
    message="Phone number must start with +98 and be followed by 9 digits.",
)

# Validator for national code (Iran's national code - 10 digits)
national_code_validator = RegexValidator(
    regex=r"^\d{10}$",  # Exactly 10 digits
    message="National code must be exactly 10 digits and contain only numbers.",
)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ("customer", "Customer"),
        ("store_owner", "Store Owner"),
        ("admin", "Admin"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[national_code_validator],
    )
    store_logo = models.ImageField(
        upload_to="store_logos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"]),
            validate_file_size,
        ],
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=15, unique=True, validators=[phone_number_validator]
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default="customer")
    active_mode = models.BooleanField(default=True)
    store_industry = models.ForeignKey(
        "Store_Industry", on_delete=models.CASCADE, null=True, blank=True
    )
    store_description = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    objects = CustomUserManeger()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username
