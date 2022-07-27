from tortoise import models, fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class ManagerModel(models.Model):
    email = fields.CharField(max_length=64)
    hashed_password = fields.CharField(max_length=128)


Tortoise.init_models(['models.manager'], 'models')
Manager_Pydantic = pydantic_model_creator(ManagerModel, name='Manager')
ManagerIn_Pydantic = pydantic_model_creator(ManagerModel, name="ManagerIn", exclude=('id',))
