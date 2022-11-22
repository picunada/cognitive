import regex as re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import ValidationError
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from cognitive.api.v1.serializers.organization import OrganizationFullSerializer


User = get_user_model()


class UserFullSerializer(serializers.ModelSerializer):
    organization = OrganizationFullSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'email', 'first_name',
                  'last_name', 'role', 'organization', 'created_at')
        read_only_fields = ('id', 'email', 'is_email_proved')
        model = User


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for create user endpoint.
    """
    token = serializers.SerializerMethodField()
    confirm_password = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'organization', 'password', 'confirm_password',
                  'token',)
        read_only_fields = ('id', 'token')
        extra_kwargs = {'password': {'write_only': True}, 'rsa_key': {'write_only': True}}

    @staticmethod
    def get_token(user):
        # Create JWT token for new user
        token = RefreshToken.for_user(user)

        return {'refresh': str(token),
                'access': str(token.access_token)}

    def create(self, data):

        user = self.context['request'].user
        new_user_role = data.get('role')
        new_user_organization = data.get('organization')

        if user.role == User.Role.MANAGER and new_user_role in [User.Role.ADMINISTRATOR, User.Role.MANAGER]:
            raise ValidationError({'role': ['not enough permissions']})

        if user.role == User.Role.MANAGER and new_user_organization not in user.organization:
            raise ValidationError({'role': ['not enough permissions']})

        if new_user_role == User.Role.CLIENT and new_user_organization.lenth() > 1:
            raise ValidationError({'role': ['user with this role can be added to one organization only']})

        if not data.get('password') or not data.get('confirm_password'):
            raise ValidationError({"password": ['Please enter a password and confirm it.']})

        if data.get('password') != data.get('confirm_password'):
            raise ValidationError({"password": ["Those passwords don't match."]})

        if re.search(r'\p{IsCyrillic}', data.get('password')):
            raise ValidationError({"password": ["Password should not contain cyrillic symbols."]})

        password = data.pop('password')
        data.pop('confirm_password')

        if len(password) < 8:
            raise ValidationError({"password": ['Password too short']})

        user = super().create(data)

        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        user = self.context['request'].user
        new_user_role = validated_data.get('role')
        new_user_organization = validated_data.get('organization')

        if user.role == User.Role.MANAGER \
                and validated_data.get('role') in [User.Role.ADMINISTRATOR, User.Role.MANAGER]:
            raise ValidationError({'role': ['not enough permissions']})

        if user.role == User.Role.MANAGER and new_user_organization not in user.organization:
            raise ValidationError({'role': ['not enough permissions']})

        if new_user_role == User.Role.CLIENT and new_user_organization.lenth() > 1:
            raise ValidationError({'role': ['user with this role can be added to the one organization only']})

        user = super().update(instance, validated_data)
        user.save()

        return user


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise exceptions.ValidationError(
                f'User with email {value} not found.')
        return value

    def save(self):
        request = self.context.get('request')
        email = request.data['email']
        user = User.objects.get(email__iexact=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = f'{settings.SITE_URL}/restore/{uid}/{token}'
        # context = {'email': email, 'url': url}
        # send_password_reset_email_task.delay(context)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(allow_blank=False)
    token = serializers.CharField(allow_blank=False)
    password1 = serializers.CharField(allow_blank=False, max_length=128)
    password2 = serializers.CharField(allow_blank=False, max_length=128)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            self.user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': ['Passwords do not match']})
        validate_password(attrs['password2'], self.user)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})
        return attrs

    def save(self):
        password1 = self.validated_data['password1']
        self.user.set_password(password1)
        self.user.save()
        return self.user
