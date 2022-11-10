import uuid

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoLastModifiedField, AutoCreatedField
from django.db import models

from .managers import DeletedManager


class UUIDModel(models.Model):
    id = models.UUIDField(_('ID'), default=uuid.uuid4,
                          primary_key=True, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField(_('created'))
    updated_at = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    created_at = models.DateTimeField(
        _('created at'), db_index=True, default=timezone.now)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    deleted_at = models.DateTimeField(
        _('deleted at'), null=True, blank=True, editable=False)

    objects = DeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class CreatedUpdatedDeletedModel(TimeStampedModel, DeletedModel):
    class Meta:
        abstract = True


class CreatedDeletedModel(CreatedModel, DeletedModel):
    class Meta:
        abstract = True
