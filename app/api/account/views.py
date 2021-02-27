from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as DefaultTokenObtainPairView,
    TokenRefreshView as DefaultTokenRefreshView
)

from app.account.models import User
from app.api.account.schemas import (
    TokenObtainPairSchema,
    TokenRefreshSchema
)
from app.api.account.serializers import (
    TokenObtainPairRequestSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshRequestSerializer,
    TokenRefreshResponseSerializer,
    UserSerializer,
    ChangePasswordSerializer, UserUpdateSerializer,
)
from app.api.shared.schemas import AutoSchema


class TokenObtainPairView(DefaultTokenObtainPairView):
    """
    get: Get User info of authenticated user with JWT
    post: Obtain a refresh and access token with username and password
    """
    serializer_class = TokenObtainPairRequestSerializer
    schema = TokenObtainPairSchema()

    def post(self, request, *args, **kwargs):
        request_serializer = self.get_serializer(data=request.data)

        try:
            request_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_serializer = TokenObtainPairResponseSerializer(request_serializer.validated_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method.lower() == 'get':
            return [IsAuthenticated()]
        return []

    def get_authenticators(self):
        if self.request.method.lower() == 'get':
            return [SessionAuthentication(), JWTAuthentication()]
        return []


class TokenRefreshView(DefaultTokenRefreshView):
    """
    post: Refresh access token with already existing refresh token
    """
    serializer_class = TokenRefreshRequestSerializer
    schema = TokenRefreshSchema()

    def post(self, request, *args, **kwargs):
        request_serializer = self.get_serializer(data=request.data)
        try:
            request_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_serializer = TokenRefreshResponseSerializer(
            request_serializer.validated_data
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=['Users'])
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        super(UserViewSet, self).perform_create(serializer)
        user = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])

    @action(methods=['post'], detail=True, url_name='change-password', url_path='password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ChangePasswordSerializer(instance=instance,
                                              data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        serializer_mappings = {
            'update': UserUpdateSerializer,
            'partial_update': UserUpdateSerializer,
            'change_password': ChangePasswordSerializer
        }

        return serializer_mappings.get(self.action, UserSerializer)
