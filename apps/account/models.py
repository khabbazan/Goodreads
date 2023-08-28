from django.db import models
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from apps.account.managers import CustomUserManager
from apps.account.validators import user_validation
from apps.account.validators import auther_validation
from apps.book.models import Shelf



######################### User ###################

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(_("Phone Number"), max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ["phone_number"]

    def __str__(self):
        return self.phone_number

    def clean(self):
        user_validation(**vars(self))
        return super().clean()

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.shelves.all():
            for shelf_name in Shelf.ShelfName.values:
                Shelf.objects.create(name=shelf_name, user=self)
        return True


######################### Author ###################

class Author(User):
    first_name = models.CharField(_("First Name"), max_length=200, blank=False)
    last_name = models.CharField(_("Last Name"), max_length=200, blank=False)

    class Meta:
        db_table = "Author"
        ordering = ["phone_number"]

    @property
    def full_name(self):
        return f"{self.first_name},{self.last_name}"

    def clean(self):
        auther_validation(**vars(self))
        return super().clean()

    def __str__(self):
        return f"[AUTHER]-{self.phone_number}"

######################### Relation ###################

class Relation(models.Model):
    followers = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.followers} -> {self.following}"
