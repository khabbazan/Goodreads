from django.contrib.auth.base_user import BaseUserManager


from apps.account.validators import base_user_validation
from apps.account.validators import staff_user_validation

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **kwargs):
        """
        Create and save a user with the given phone_number and password.
        """
        base_user_validation(phone_number, password)
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **kwargs):
        """
        Create and save a SuperUser with the given phone_number and password.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        staff_user_validation(
            kwargs.get("is_staff"),
            kwargs.get("is_superuser"),
        )

        return self.create_user(phone_number, password, **kwargs)
