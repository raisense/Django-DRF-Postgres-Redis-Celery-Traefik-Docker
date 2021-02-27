from django.contrib.auth.models import AbstractUser


# if customization needed for default django user model
class User(AbstractUser):
    pass
