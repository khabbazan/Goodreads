from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.

    This manager provides methods for creating users and superusers with the given phone number and password.

    Methods:
        - create_user(phone_number, password, **kwargs):
            Create and save a user with the given phone_number and password.

        - create_superuser(phone_number, password, **kwargs):
            Create and save a SuperUser with the given phone_number and password.

        - delete(*args, **kwargs):
            De-activate objects instead of physically deleting them.

    """
    def create_user(self, phone_number, password, **kwargs):
        """
        Create and save a user with the given phone_number and password.

        Args:
            phone_number (str): The user's phone number.
            password (str): The user's password.
            **kwargs: Additional fields to set on the user model.

        Returns:
            User: The created user instance.
        """
        user = self.model(phone_number=phone_number, password=password, **kwargs)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **kwargs):
        """
        Create and save a SuperUser with the given phone_number and password.

        Args:
            phone_number (str): The user's phone number.
            password (str): The user's password.
            **kwargs: Additional fields to set on the user model.

        Returns:
            User: The created SuperUser instance.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self.create_user(phone_number, password, **kwargs)

    def delete(self, *args, **kwargs):
        """
        De-activate objects instead of physically deleting them.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.update(is_active=False)

class CustomAuthorManager(Manager):
    """
    Custom manager for the Author model (placeholder).

    This manager can be extended with custom methods for the Author model if needed.
    """
    pass

class CustomRelationManager(Manager):
    """
    Custom manager for the Relation model (placeholder).

    This manager can be extended with custom methods for the Relation model if needed.
    """
    pass
