from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)

GENDERS = [
    ('male', 'male'),
    ('female', 'female'),
]


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Valid email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=256,
        unique=True
    )
    username = models.CharField(max_length=64)
    gender = models.CharField(max_length=8, choices=GENDERS)

    name = models.CharField(max_length=256, blank=True, null=True)
    legal = models.CharField(max_length=256, blank=True, null=True)
    founded = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=256, blank=True, null=True)
    employees = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    parent_domain = models.CharField(max_length=256, blank=True, null=True)
    ultimate_parent_domain = models.CharField(max_length=256, blank=True, null=True)
    tags = models.CharField(max_length=256, blank=True, null=True)
    industry = models.CharField(max_length=256, blank=True, null=True)
    sector = models.CharField(max_length=256, blank=True, null=True)
    sic_code = models.CharField(max_length=256, blank=True, null=True)
    naics_code = models.CharField(max_length=256, blank=True, null=True)
    technologies = models.CharField(max_length=256, blank=True, null=True)
    technology_categories = models.CharField(max_length=256, blank=True, null=True)
    alexa_global_rank = models.CharField(max_length=256, blank=True, null=True)
    crunchbase = models.CharField(max_length=256, blank=True, null=True)
    twitter = models.CharField(max_length=256, blank=True, null=True)
    facebook = models.CharField(max_length=256, blank=True, null=True)
    linkedin = models.CharField(max_length=256, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    is_superuser = models.BooleanField(default=False)
