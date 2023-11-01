from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.book.managers import CustomBookManager
from apps.book.managers import CustomTagManager
from apps.book.query_sets import BookQuerySet
from apps.book.query_sets import TagQuerySet
from apps.book.validators import book_validation


class Tag(models.Model):
    """
    Model class for book tags.

    Fields:
        - TAG (tuple): Choices for tag types.
        - name (CharField): The name of the tag.

    Methods:
        - __str__(): Returns the name of the tag as a string.
    """

    TAG = (
        ("NEW", _("NEW")),
        ("TREND", _("TREND")),
        ("DISCOUNT", _("DISCOUNT")),
    )

    name = models.CharField(max_length=20, choices=TAG)

    objects = CustomTagManager.from_queryset(TagQuerySet)()

    def __str__(self):
        """
        String representation of the tag.

        Returns:
            str: A string representing the tag.
        """
        return self.name


class Book(models.Model):
    """
    Model class for books.

    Fields:
        - ISBN (CharField): International Standard Book Number.
        - title (CharField): Title of the book.
        - description (TextField): Description of the book.
        - is_active (BooleanField): Indicates whether the book is active.
        - tags (ManyToManyField): Many-to-Many relationship with 'Tag' model.
        - create_time (DateTimeField): Timestamp for creation.
        - modified_time (DateTimeField): Timestamp for modification.

    Methods:
        - __str__(): Returns the title of the book as a string.
        - clean(): Validates book information.
        - clean_fields(): Cleans and validates model fields.
        - save(): Saves the book instance after validation.
    """

    ISBN = models.CharField(_("ISBN"), max_length=100, unique=True)
    title = models.CharField(_("book title"), max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(_("is_active"), default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    objects = CustomBookManager.from_queryset(BookQuerySet)()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        """
        String representation of the book.

        Returns:
            str: A string representing the book title.
        """
        return self.title

    def clean(self):
        """
        Validates and cleans the book model's fields.

        Returns:
            None
        """
        book_validation(**vars(self))
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
        book_validation(**fields)
        return {k: v for k, v in fields.items() if v is not None}

    def save(self, *args, **kwargs):
        """
        Saves the book instance after validation.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if the instance was successfully saved.
        """
        self.clean()
        return super().save(*args, **kwargs)


class BookAuthor(models.Model):
    """
    Model class to represent the relationship between books and authors.

    Fields:
        - book (ForeignKey): The associated book.
        - author (ForeignKey): The associated author.

    Methods:
        - __str__(): Returns a string representation of the relationship.
    """

    book = models.ForeignKey(Book, related_name="authors", on_delete=models.CASCADE)
    author = models.ForeignKey(to="account.Author", related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book}: {self.author}"


class Shelf(models.Model):
    """
    Model class for bookshelves.

    Fields:
        - ShelfName (tuple): Choices for shelf names.
        - name (CharField): The name of the shelf.
        - user (ForeignKey): The associated user.

    Methods:
        - __str__(): Returns a string representation of the shelf.
    """

    ShelfName = (
        ("R", _("Read")),
        ("CR", _("Currently Reading")),
        ("WR", _("Want to Read")),
    )

    name = models.CharField(_("shelf name"), max_length=2, choices=ShelfName, default="WR")
    user = models.ForeignKey(to="account.User", related_name="shelves", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shelves"

    def __str__(self):
        """
        String representation of the shelf.

        Returns:
            str: A string representing the shelf.
        """
        return f"{self.user}[{self.get_name_display()}]"


class BookShelf(models.Model):
    """
    Model class to represent the relationship between users, books, and bookshelves.

    Fields:
        - user (ForeignKey): The associated user.
        - book (ForeignKey): The associated book.
        - shelf (ForeignKey): The associated shelf.
        - create_time (DateTimeField): Timestamp for creation.
        - modified_time (DateTimeField): Timestamp for modification.

    Methods:
        - __str__(): Returns a string representation of the relationship.
    """

    user = models.ForeignKey(to="account.User", related_name="bookshelf_users", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="bookshelf_books", on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, related_name="bookshelf_shelves", on_delete=models.CASCADE)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Book shelves"

    def __str__(self):
        """
        String representation of the bookshelf.

        Returns:
            str: A string representing the bookshelf.
        """
        return f"{self.user} -> {self.book}:{self.shelf}"
