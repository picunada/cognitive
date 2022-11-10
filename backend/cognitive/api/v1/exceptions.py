from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, Throttled


class APIErrorFormat:
    code = None
    detail = None
    payload = None

    def as_dict(self) -> dict:
        json = {
            'code': self.code,
            'message': self.detail_format(),
        }
        return json

    def __str__(self) -> str:
        return f'{self.code}: {self.detail_format()}'

    def detail_format(self) -> str:
        if self.payload is not None and isinstance(self.payload, dict):
            return self.detail.format(**self.payload)
        return self.detail

    @classmethod
    def from_exception(cls, exc: 'rest_framework.exceptions.APIException') -> 'APIError':
        if isinstance(exc, (APIError, ValidationAPIError)):
            return exc

        detail = exc.default_detail
        if isinstance(exc, Throttled):
            detail = exc.detail

        return APIError(detail=detail, code=exc.default_code)


class APIError(APIException, APIErrorFormat):
    """
    Use this class to provide error information for api endpoints.
    Collects in utils.mixins.APIViewErrorMixin
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'api_error'
    # Translators: raw text - 'An API error occurred.'
    default_detail = _('api_error')

    def __init__(
            self,
            detail: Optional[str] = None,
            code: Optional[str] = None,
            payload: Optional[dict] = None,
    ) -> None:
        super().__init__(detail, code)
        self.payload = payload
        self.code = code or self.default_code


class ValidationAPIError(APIException, APIErrorFormat):
    """
    Validation error with simplified structure: detail should be str.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_field = None

    def __init__(
            self,
            detail: Optional[str] = None,
            code: Optional[str] = None,
            field: Optional[str] = None,
            payload: Optional[dict] = None,
    ):
        self.field = field or self.default_field
        self.code = code or self.default_code
        self.detail = detail or self.default_detail
        self.payload = payload

    def as_dict(self) -> dict:
        json = super().as_dict()

        if self.field is not None:
            json['field'] = self.field

        return json
