from app.api.account.serializers import (
    TokenObtainPairRequestSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshRequestSerializer,
    TokenRefreshResponseSerializer
)
from app.api.shared.schemas import AutoSchema


class TokenObtainPairSchema(AutoSchema):
    def get_operation_id(self, path, method):
        return 'obtainAccessRefreshToken' if method.lower() == 'post' else 'getUserInfo'

    def get_tags(self, path, method):
        return ['Me']

    def get_request_serializer(self, path, method):
        return TokenObtainPairRequestSerializer()

    def get_response_serializer(self, path, method):
        return TokenObtainPairResponseSerializer()


class TokenRefreshSchema(AutoSchema):
    def get_operation_id(self, path, method):
        return 'refreshAccessToken'

    def get_tags(self, path, method):
        return ['Me']

    def get_request_serializer(self, path, method):
        return TokenRefreshRequestSerializer()

    def get_response_serializer(self, path, method):
        return TokenRefreshResponseSerializer()
