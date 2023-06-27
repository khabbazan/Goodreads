from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.account.managers import CustomUserManager


######################### User ###################

class User(AbstractUser):
    username = None
    phone_number = models.CharField(_("phone number"), max_length=50, unique=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ["phone_number"]

    def __str__(self):
        return self.phone_number

######################### Author ###################

class Author(User):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        db_table = "Author"
        ordering = ["phone_number"]

    def __str__(self):
        return f"[AUTHER]-{self.phone_number}"

######################### Relation ###################

class Relation(models.Model):
    followers = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.followers} -> {self.following}"
