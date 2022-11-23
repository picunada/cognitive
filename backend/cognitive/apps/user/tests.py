from rest_framework.test import APITestCase
from rest_framework import status
from cognitive.apps.organization.models import Organization
from cognitive.apps.user.factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken
from cognitive.apps.user.models import User
from cognitive.apps.organization.factory import OrganizationFactory
from cognitive.apps.core.utils import to_dict

BASE_URL = "http://127.0.0.1:8000/api/v1"


class UserTestCases(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = UserFactory.create_batch(3)
        cls.admin_user = User.objects.create(
            first_name='Admin', last_name='test', role=User.Role.ADMINISTRATOR, email="admin@example.com")
        cls.manager_user = User.objects.create(
            first_name='Client', last_name='test', role=User.Role.MANAGER, email="manager@example.com")
        cls.client_user = User.objects.create(
            first_name='Client', last_name='test', role=User.Role.CLIENT, email="client@example.com")
        cls.organization = OrganizationFactory.build(
            status=Organization.Status.ACTIVE, users=cls.users)
        cls.user = UserFactory.build(
            organization=cls.organization, role=User.Role.CLIENT)
        cls.user_url = f'{BASE_URL}/user/'
        cls.organization_url = f'{BASE_URL}/organization/'
        cls.base64mock = {
            "message": "QL0AFWMIX8NRZTKeof9cXsvbvu8="
        }

    def test_admin_create(self):
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = to_dict(self.user)
        data['password'] = 'testtesttest'
        data['confirm_password'] = 'testtesttest'

        response = self.client.post(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        query = User.objects.filter(first_name=self.user.first_name)
        self.assertEqual(query.count(), 1)

    def test_admin_update(self):
        user = UserFactory(role=User.Role.CLIENT)
        query = User.objects.filter(first_name=user.first_name)
        usr = query.get()
        self.assertEqual(usr.role, User.Role.CLIENT)

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = to_dict(user)
        data['role'] = User.Role.MANAGER

        response = self.client.patch(
            f'{self.user_url}{user.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = User.objects.filter(first_name=user.first_name)
        usr = query.get()
        self.assertEqual(usr.role, User.Role.MANAGER)

    def test_admin_delete(self):
        user = UserFactory(role=User.Role.CLIENT)
        query = User.objects.filter(first_name=user.first_name)
        self.assertEqual(query.count(), 1)

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.delete(
            f'{self.user_url}{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        query = User.objects.filter(first_name=user.first_name)
        self.assertEqual(query.count(), 0)

    def test_admin_generate_api_key(self):
        organization = OrganizationFactory()

        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(
            f'{self.organization_url}{organization.id}/generate_key/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_cant_create_client_for_not_own_organization(self):
        test_own_organization = OrganizationFactory(
            users=(self.manager_user, ))
        test_not_own_organization = OrganizationFactory()

        test_user_for_own = UserFactory.build(role=User.Role.CLIENT)
        test_user_for_not_own = UserFactory.build(role=User.Role.CLIENT)

        refresh = RefreshToken.for_user(self.manager_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data_own = to_dict(test_user_for_own)
        data_own['password'] = 'testtesttest'
        data_own['confirm_password'] = 'testtesttest'
        data_own['organization'] = [test_own_organization.id, ]

        data_not_own = to_dict(test_user_for_not_own)
        data_not_own['password'] = 'testtesttest'
        data_not_own['confirm_password'] = 'testtesttest'
        data_not_own['organization'] = [test_not_own_organization.id, ]

        # Should return 201 CREATED status
        response = self.client.post(
            f'{self.user_url}', data_own)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Should return 400 BAD REQUEST status
        response = self.client.post(
            f'{self.user_url}', data_not_own)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_cant_create_user_not_with_client_role(self):
        test_organization = OrganizationFactory(
            users=(self.manager_user, ))

        client = UserFactory.build(role=User.Role.CLIENT)
        manager = UserFactory.build(role=User.Role.MANAGER)
        admin = UserFactory.build(role=User.Role.ADMINISTRATOR)

        refresh = RefreshToken.for_user(self.manager_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data_client = to_dict(client)
        data_client['password'] = 'testtesttest'
        data_client['confirm_password'] = 'testtesttest'
        data_client['organization'] = [test_organization.id, ]

        # Should return 201 CREATED status
        response = self.client.post(
            f'{self.user_url}', data_client)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_manager = to_dict(manager)
        data_manager['password'] = 'testtesttest'
        data_manager['confirm_password'] = 'testtesttest'
        data_manager['organization'] = [test_organization.id, ]

        # Should return 400 BAD REQUEST status
        response = self.client.post(
            f'{self.user_url}', data_manager)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data_admin = to_dict(admin)
        data_admin['password'] = 'testtesttest'
        data_admin['confirm_password'] = 'testtesttest'
        data_admin['organization'] = [test_organization.id, ]

        # Should return 400 BAD REQUEST status
        response = self.client.post(
            f'{self.user_url}', data_admin)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_cant_delete_user_from_not_own_organization(self):
        own_client = UserFactory(role=User.Role.CLIENT)
        not_own_client = UserFactory(role=User.Role.CLIENT)

        test_own_organization = OrganizationFactory(
            users=(self.manager_user, own_client))
        test_not_own_organization = OrganizationFactory(
            users=(not_own_client, ))

        refresh = RefreshToken.for_user(self.manager_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Should return 201 CREATED status
        response = self.client.delete(
            f'{self.user_url}{own_client.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Should return 201 CREATED status
        response = self.client.delete(
            f'{self.user_url}{not_own_client.id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_cant_update_user_from_not_own_organization(self):
        own_client = UserFactory(role=User.Role.CLIENT)
        not_own_client = UserFactory(role=User.Role.CLIENT)

        test_own_organization = OrganizationFactory(
            users=(self.manager_user, own_client))
        test_not_own_organization = OrganizationFactory(
            users=(not_own_client, ))

        refresh = RefreshToken.for_user(self.manager_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data_own = to_dict(own_client)
        data_own['first_name'] = 'test1'

        # Should return 201 CREATED status
        response = self.client.patch(
            f'{self.user_url}{own_client.id}/', data_own)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = User.objects.filter(id=own_client.id)
        self.assertEqual(query.get().first_name, 'test1')

        # Should return 201 CREATED status
        response = self.client.patch(
            f'{self.user_url}{not_own_client.id}/', )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
