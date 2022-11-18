from django.db import models
from cognitive.apps.organization.models import Organization
from cognitive.apps.core.models import CreatedDeletedModel


class Transaction(CreatedDeletedModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="transactions")
