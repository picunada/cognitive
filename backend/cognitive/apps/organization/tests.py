from rest_framework.test import APITestCase
from rest_framework import status
from cognitive.apps.organization.models import Organization, Status
from cognitive.apps.user.factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken
from cognitive.apps.user.models import Roles, User
from .factory import OrganizationFactory
from cognitive.apps.core.utils import to_dict

BASE_URL = "http://127.0.0.1:8000/api/v1"


class OrganizationTestCases(APITestCase):

    # user_saved = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = UserFactory.create_batch(3)
        cls.admin_user = User.objects.create(
            first_name='Admin', last_name='test', role=Roles.ADMINISTRATOR, email="admin@example.com")
        cls.client_user = User.objects.create(
            first_name='Client', last_name='test', role=Roles.CLIENT, email="client@example.com")
        cls.organization = OrganizationFactory.build(
            status=Status.ACTIVE, users=cls.users)
        cls.organization_url = f'{BASE_URL}/organization/'
        cls.base64mock = {
            "message": "QL0AFWMIX8NRZTKeof9cXsvbvu8="
        }

    def test_create_organization(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = to_dict(self.organization)

        response = self.client.post(self.organization_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        query = Organization.objects.filter(name=self.organization.name)
        self.assertEqual(query.count(), 1)

    def test_update_organization(self):
        organization = OrganizationFactory()

        query = Organization.objects.filter(name=organization.name)
        org = query.get()
        self.assertEqual(org.status, Status.ACTIVE)

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = to_dict(organization)
        data['status'] = Status.BLOCKED

        response = self.client.patch(
            f'{self.organization_url}{organization.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = Organization.objects.filter(name=organization.name)
        org = query.get()
        self.assertEqual(org.status, Status.BLOCKED)

    def test_delete_organization(self):
        organization = OrganizationFactory()

        query = Organization.objects.filter(name=organization.name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.delete(
            f'{self.organization_url}{organization.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        query = Organization.objects.filter(name=organization.name)
        org = query.get()
        self.assertNotEqual(org.deleted_at, None)

    def test_sign_message(self):
        organization = OrganizationFactory(
            balance=100, users=(self.client_user, ))

        query = Organization.objects.filter(name=organization.name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.client_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.get(
            f'{self.organization_url}{organization.id}/generate_key/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_X_API_KEY=response.json(),
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.post(
            f'{self.organization_url}sign_message/', self.base64mock)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_message_with_low_balance_should_return_400(self):
        organization = OrganizationFactory(
            balance=0, users=(self.client_user, ))

        query = Organization.objects.filter(name=organization.name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.client_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.get(
            f'{self.organization_url}{organization.id}/generate_key/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_X_API_KEY=response.json(),
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.post(
            f'{self.organization_url}sign_message/', self.base64mock)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_message_with_blocked_status_should_return_400(self):
        organization = OrganizationFactory(
            balance=100, status=Status.BLOCKED, users=(self.client_user, ))

        query = Organization.objects.filter(name=organization.name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.client_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.get(
            f'{self.organization_url}{organization.id}/generate_key/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_X_API_KEY=response.json(),
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.post(
            f'{self.organization_url}sign_message/', self.base64mock)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_message_with_wrong_message_should_return_400(self):
        organization = OrganizationFactory(
            balance=100, status=Status.ACTIVE, users=(self.client_user, ))

        query = Organization.objects.filter(name=organization.name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.client_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        response = self.client.get(
            f'{self.organization_url}{organization.id}/generate_key/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_X_API_KEY=response.json(),
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        data = self.base64mock
        data['message'] = 'test'

        response = self.client.post(
            f'{self.organization_url}sign_message/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.json())
