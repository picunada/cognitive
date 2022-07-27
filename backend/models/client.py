from enum import Enum

from tortoise import models, fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class StatusEnum(str, Enum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


class ClientModel(models.Model):
    key = fields.CharField(max_length=1024)
    status: StatusEnum = fields.CharEnumField(StatusEnum, default=StatusEnum.ACTIVE)
    count = fields.IntField()


class KeyModel(models.Model):
    client = fields.ForeignKeyField('models.ClientModel', null=False, related_name='api_key')
    api_key = fields.CharField(max_length=64)


Tortoise.init_models(['models.client'], 'models')
Client_Pydantic = pydantic_model_creator(ClientModel, name='Client')
ClientIn_Pydantic = pydantic_model_creator(ClientModel, name="ClientIn", exclude=('id', 'api_key'))
APIKey_Pydantic = pydantic_model_creator(KeyModel, name="APIKey")
