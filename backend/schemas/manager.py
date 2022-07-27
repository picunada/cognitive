from pydantic import BaseModel, validator, constr


class ManagerCreate(BaseModel):
    email: str
    password: constr(min_length=8)
    password2: constr(min_length=8)

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return
