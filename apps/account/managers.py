from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q, QuerySet

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **kwargs):
        """
        Create and save a user with the given phone_number and password.
        """
        user = self.model(phone_number=phone_number, password=password, **kwargs)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **kwargs):
        """
        Create and save a SuperUser with the given phone_number and password.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self.create_user(phone_number, password, **kwargs)



class UserQuerySet(QuerySet):
    """
    Manager and queryset methods
    """

    def search(self, query):
        """
        Search in listed items of a user by `__icontains` policy in phone numbers.
        """
        return self.filter(Q(phone_number__icontains=query)).distinct() if query else self


CustomUserManager = CustomUserManager.from_queryset(UserQuerySet)
