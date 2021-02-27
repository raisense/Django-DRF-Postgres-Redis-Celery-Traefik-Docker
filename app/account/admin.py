from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.admin import admin

from app.account.models import User


class UserAdmin(DefaultUserAdmin):
    pass


admin.site.register(User, UserAdmin)
