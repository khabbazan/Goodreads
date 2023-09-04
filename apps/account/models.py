from django.db import models
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from apps.account.managers import CustomUserManager
from apps.account.managers import CustomAuthorManager
from apps.account.query_sets import UserQuerySet
from apps.account.query_sets import AuthorQuerySet
from apps.account.validators import user_validation
from apps.account.validators import author_validation
from apps.book.models import Shelf
from apps.extension.models import Image



######################### User ###################

class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ("MALE", _("MALE")),
        ("FEMALE", _("FEMALE")),
    )

    phone_number = models.CharField(_("Phone Number"), max_length=50, unique=True)
    is_staff = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)
    is_superuser = models.BooleanField(null=True, default=True)
    is_author = models.BooleanField(null=True, default=False)
    gender = models.CharField(max_length=6, choices=GENDER)
    _avatar = GenericRelation(Image)

    date_joined = models.DateTimeField(null=True, default=timezone.now)

    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager.from_queryset(UserQuerySet)()

    class Meta:
        ordering = ["phone_number"]

    @property
    def avatar(self):
        if self._avatar.count():
            return self._avatar.last()
        else:
            return False

    @avatar.setter
    def avatar(self, new_avatar):
        # remove old avatars
        if self._avatar.count():
            old_avatar = self._avatar.model.objects.first()
            old_avatar.delete()

        # create new avatar
        image_instance = self._avatar.model(user=self, content_object=self, original_image=new_avatar)
        image_instance.save()


    def __str__(self):
        return self.phone_number

    def clean(self):
        user_validation(**vars(self))
        return super().clean()

    @classmethod
    def clean_fields(cls, *args, **kwargs):
        fields = {**kwargs}
        user_validation(**fields)
        return {k: v for k, v in fields.items() if v is not None}

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.clean()

        try:
            identify_hasher(self.password)
        except ValueError:
            self.set_password(self.password)

        super().save(*args, **kwargs)
        if not self.shelves.all():
            for shelf_name in Shelf.ShelfName.values:
                Shelf.objects.create(name=shelf_name, user=self)

        return True


######################### Author ###################

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(_("First Name"), max_length=200, blank=False)
    last_name = models.CharField(_("Last Name"), max_length=200, blank=False)

    objects = CustomAuthorManager.from_queryset(AuthorQuerySet)()

    class Meta:
        db_table = "Author"
        ordering = ["last_name"]

    @property
    def full_name(self):
        return f"{self.first_name},{self.last_name}"

    def clean(self):
        author_validation(**vars(self))
        return super().clean()

    @classmethod
    def clean_fields(cls, *args, **kwargs):
        fields = {**kwargs}
        author_validation(**fields)
        return {k: v for k, v in fields.items() if v is not None}

    def save(self, *args, **kwargs):
        self.user.is_author = True
        self.user.save()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"[AUTHER]-{self.user.phone_number}"

######################### Relation ###################

class Relation(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.phone_number} follows {self.following.phone_number}"
