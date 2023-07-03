from django.db import models
from django.utils.translation import gettext_lazy as _

######################### Book #######################

class Book(models.Model):

    ISBN = models.CharField(_("ISBN"), max_length=100, unique=True)
    title = models.CharField(_("book title"), max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


######################### Book Author ################

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, related_name='authors', on_delete=models.CASCADE)
    author = models.ForeignKey(to='account.Author', related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book}: {self.author}"

######################### Shelf ######################

class Shelf(models.Model):

    class ShelfName(models.TextChoices):
        READ = 'R', _('Read')
        CURRENTLY_READING = 'CR', _('Currently Reading')
        WANT_TO_READ = 'WR', _('Want to Read')

    name = models.CharField(_("shelf name"), max_length=2, choices=ShelfName.choices, default=ShelfName.WANT_TO_READ)
    user = models.ForeignKey(to='account.User', related_name='shelves', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shelves"
    def __str__(self):
        return f"{self.get_name_display()}"

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
