from .models import Organization, Status
from faker import Faker as FakerClass
from factory import django, Faker, post_generation

STATUS_VALUES = [x[0] for x in Status.choices]
fake = FakerClass()


class OrganizationFactory(django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = Faker('company')
    hashed_key = '-----BEGIN RSA PRIVATE KEY----- MIICWwIBAAKBgQC9918sD6fTeh4AS0Ewc3oE6VHocos/Gy8kLFRzHK98qXNemQYuXFTN0ZDdd07+\
    k2za0oZSDby8DzeJuUSRx+F2iejzNBiDCSJIIBEW4NvXxlzCFlDq7hizrZofVL1tvOhlKXwzaEKt R8Xx9HrNevwNdVqohTbvUTbwFFIrysYSeQIBAwKBgH6k\
    6h1fxTemvqrc1iBM/ANGNpr3B39ndMLI OEy9ylMboj8QrsmS4zPhCz5Pif8M8zyMWYwJKH1felvQ2GEv66M15HFb7XLVNabs62nDRf9aSH2V 8FPvt336WiL\
    NksHmkOcjMTRqacy6brm9Yzld4YQRyq6qh/4q2gZoV6YHTEKjAkEA3q/25mfLvhlj Bmnl3rf2qJaxiKqC5G3PsDG/zcCjPXPtnClnKYXSLPT44C6KtZYYrM6\
    uXpp+whoDElE/EkFb5wJB ANpiUkPMiws4arZGEl064hZZVCy96iIXpwXhK1Kgp6WbHNiI/Z8eKAMq4ng3bLiTrq3b9CbQc07V 42V9c62SUp8CQQCUdU9ERT\
    J+u5dZm+6UeqRwZHZbHFdC89/Ky9Uz1cIo9/O9cO9xA+FzTftAHwcj uWXIicmUZv8sEVdhi39hgOfvAkEAkZbhgohcsiWceYQMPidBZDuNcylGwWUaA+tyNx\
    XFGRITOwX+ ahQarMdBpXpIew0fHpKixIr3iePs7lOic7bhvwJAQ0tVwAkR1odDV20TvrDUn0rb2koz4dIGzjQC +v17BQjFwStptgYrOV3jqM9podzCjx+G\
    eAxxEtMmcgAUDXCiSg== -----END RSA PRIVATE KEY-----'
    status = 'active'
    balance = fake.random_int(min=0, max=1000)

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)
