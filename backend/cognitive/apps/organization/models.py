from django.db import models
from cognitive.apps.core.models import CreatedDeletedModel
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager
from rest_framework_api_key.crypto import KeyGenerator


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
    balance = models.PositiveSmallIntegerField(default=0)


class OrganizationAPIKeyManager(BaseAPIKeyManager):
    key_generator = KeyGenerator(prefix_length=8, secret_key_length=32)


class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="api_keys",)

    objects = OrganizationAPIKeyManager()

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Organization API key"
        verbose_name_plural = "Organization API keys"
