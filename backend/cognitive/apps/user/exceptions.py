from django.utils.translation import gettext_lazy as _

from cognitive.api.v1.exceptions import APIError


class SuperUserAlreadyExists(APIError):
    default_code = 'user_already_exist'
    # Translators: raw text - 'User is already exist.'
    default_detail = _('user_already_exist')
