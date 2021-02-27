from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, \
    TokenRefreshSerializer

from app.account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = dict(password=dict(write_only=True))
        read_only_fields = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'user_permissions', 'groups')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'user_permissions', 'groups')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validated_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                _('Old password is wrong!')
            )
        return value

    def save(self):
        self.instance.set_password(self.validated_data.get("new_password"))
        self.instance.save()


class TokenObtainPairRequestSerializer(TokenObtainPairSerializer):
    pass


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class TokenRefreshRequestSerializer(TokenRefreshSerializer):
    pass


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
