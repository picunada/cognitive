from enum import Enum
from django.db import models
from cognitive.apps.core.models import CreatedDeletedModel
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager
from rest_framework_api_key.crypto import KeyGenerator
# Create your models here.


class Organization(CreatedDeletedModel):
    class Status(models.TextChoices):
        ACTIVE = "active"
        BLOCKED = "blocked"

    name = models.CharField(max_length=64)
    hashed_key = models.CharField(max_length=4096)
    status = models.CharField(
        max_length=64,
        choices=Status.choices,
        default=Status.ACTIVE,
    )


class OrganizationAPIKeyManager(BaseAPIKeyManager):
    key_generator = KeyGenerator(prefix_length=8, secret_key_length=32)


class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="api_keys",)

    objects = OrganizationAPIKeyManager()

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Device API key"
        verbose_name_plural = "Device API keys"
