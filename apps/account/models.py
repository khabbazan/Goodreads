
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
    """
    Represents a user in the application.

    Fields:
        phone_number (str): The user's phone number.
        is_staff (bool): Indicates if the user has staff privileges.
        is_active (bool): Indicates if the user's account is active.
        is_superuser (bool): Indicates if the user has superuser privileges.
        is_author (bool): Indicates if the user is also an author.
        gender (str): The user's gender.
        _avatar (GenericRelation): A generic relation to the 'Image' model.
        date_joined (DateTimeField): The date when the user joined.
        USERNAME_FIELD (str): The field used for authentication (phone number).
        REQUIRED_FIELDS (list): Additional required fields for authentication.
        objects (CustomUserManager): Custom manager for the 'User' model.

    Methods:
        - avatar: Property to retrieve the user's avatar.
        - clean: Validates and cleans the user model's fields.
        - clean_fields: Validates and cleans individual fields.
        - save: Saves the user instance after cleaning and hashing the password.

    """

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
        """
        Property to retrieve the user's avatar.

        Returns:
            Image or False: The user's avatar if available, False otherwise.
        """
        if self._avatar.count():
            return self._avatar.last()
        else:
            return False

    @avatar.setter
    def avatar(self, new_avatar):
        """
        Setter for the user's avatar.

        Args:
            new_avatar: The new avatar image to set.

        Returns:
            None
        """
        # remove old avatars
        if self._avatar.count():
            old_avatar = self._avatar.model.objects.first()
            old_avatar.delete()

        # create new avatar
        image_instance = self._avatar.model(user=self, content_object=self, original_image=new_avatar)
        image_instance.save()

    def clean(self):
        """
        Validates and cleans the user model's fields.

        Returns:
            None
        """
        user_validation(**vars(self))
        return super().clean()

    @classmethod
    def clean_fields(cls, *args, **kwargs):
        """
        Validates and cleans individual fields.

        Args:
            *args: Arguments to validate and clean.
            **kwargs: Keyword arguments to validate and clean.

        Returns:
            dict: Cleaned fields.
        """
        fields = {**kwargs}
        user_validation(**fields)
        return {k: v for k, v in fields.items() if v is not None}

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Saves the user instance after cleaning and hashing the password.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if the instance was successfully saved.
        """
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
    """
    Represents an author in the application.

    Fields:
        user (ForeignKey): The associated user.
        first_name (str): The author's first name.
        last_name (str): The author's last name.
        objects (CustomAuthorManager): Custom manager for the 'Author' model.

    Methods:
        - full_name: Property to retrieve the full name of the author.
        - clean: Validates and cleans the author model's fields.
        - save: Saves the author instance after setting the 'is_author' flag on the associated user.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(_("First Name"), max_length=200, blank=False)
    last_name = models.CharField(_("Last Name"), max_length=200, blank=False)

    objects = CustomAuthorManager.from_queryset(AuthorQuerySet)()

    class Meta:
        db_table = "Author"
        ordering = ["last_name"]

    @property
    def full_name(self):
        """
        Property to retrieve the full name of the author.

        Returns:
            str: The author's full name.
        """
        return f"{self.first_name}, {self.last_name}"

    def clean(self):
        """
        Validates and cleans the author model's fields.

        Returns:
            None
        """
        author_validation(**vars(self))
        return super().clean()

    @classmethod
    def clean_fields(cls, *args, **kwargs):
        """
        Validates and cleans individual fields.

        Args:
            *args: Arguments to validate and clean.
            **kwargs: Keyword arguments to validate and clean.

        Returns:
            dict: Cleaned fields.
        """
        fields = {**kwargs}
        author_validation(**fields)
        return {k: v for k, v in fields.items() if v is not None}

    def save(self, *args, **kwargs):
        """
        Saves the author instance after setting the 'is_author' flag on the associated user.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if the instance was successfully saved.
        """
        self.user.is_author = True
        self.user.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"[AUTHOR]-{self.user.phone_number}"

######################### Relation ###################

class Relation(models.Model):
    """
    Represents a relationship between users in the application.

    Fields:
        follower (ForeignKey): The user who is following.
        following (ForeignKey): The user who is being followed.
        followed_on (DateTimeField): The date when the relationship was established.

    Methods:
        - __str__: String representation of the relationship.

    """

    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the relationship.

        Returns:
            str: A string representing the relationship.
        """
        return f"{self.follower.phone_number} follows {self.following.phone_number}"
