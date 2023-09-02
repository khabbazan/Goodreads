from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.book.managers import CustomBookManager
from apps.book.query_sets import BookQuerySet
from apps.book.validators import book_validation

######################### Book #######################

class Book(models.Model):

    ISBN = models.CharField(_("ISBN"), max_length=100, unique=True)
    title = models.CharField(_("book title"), max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    objects = CustomBookManager.from_queryset(BookQuerySet)()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def clean(self):
        book_validation(**vars(self))
        return super().clean()

    @classmethod
    def clean_fields(cls, *args, **kwargs):
        fields = {**kwargs}
        book_validation(**fields)
        return True
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

######################### Book Author ################

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, related_name='authors', on_delete=models.CASCADE)
    author = models.ForeignKey(to='account.Author', related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book}: {self.author}"

######################### Shelf ######################

class Shelf(models.Model):

    ShelfName = (
        ('R', _('Read')),
        ('CR', _('Currently Reading')),
        ('WR', _('Want to Read')),
    )

    name = models.CharField(_("shelf name"), max_length=2, choices=ShelfName, default="WR")
    user = models.ForeignKey(to='account.User', related_name='shelves', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shelves"
    def __str__(self):
        return f"{self.user}[{self.get_name_display()}]"

##################### Book Shelf #####################

class BookShelf(models.Model):

    user = models.ForeignKey(to='account.User',  related_name='bookshelf_users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book,  related_name='bookshelf_books', on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, related_name='bookshelf_shelves', on_delete=models.CASCADE)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Book shelves"

    def __str__(self):
        return f"{self.user} -> {self.book}:{self.shelf}"
