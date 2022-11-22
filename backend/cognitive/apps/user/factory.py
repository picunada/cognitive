from .models import Roles, User
from typing import Any, Sequence
from faker import Faker as FakerClass
from factory import django, Faker, post_generation
fake = FakerClass()

ROLES_VALUES = [x[0] for x in Roles.choices]


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    role = Faker('random_element', elements=ROLES_VALUES)
    email = Faker('email')

    @post_generation
    def organization(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for org in extracted:
                self.organization.add(org)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else fake.password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)
