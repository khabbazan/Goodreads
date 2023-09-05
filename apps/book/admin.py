from django.contrib import admin
from apps.book.models import Book, BookAuthor, Shelf, BookShelf, Tag

###################### BookAuthor Admin ####################
@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    """
    Admin class for the 'BookAuthor' model.

    Fields:
        - list_display: Display fields in the list view.
        - search_fields: Fields available for searching.
        - list_display_links: Fields with links in the list view.
    """
    list_display = ['book', 'author']
    search_fields = ['book', 'author']
    list_display_links = ['book', 'author']

class BookInline(admin.TabularInline):
    """
    Inline class for the 'Book' model within 'BookAuthor' admin.

    Fields:
        - model: The model to be displayed inline.
        - fk_name: The foreign key to associate with.
        - extra: Number of empty forms to display for adding related objects.
    """
    model = BookAuthor
    fk_name = "book"
    extra = 1

class AuthorInline(admin.TabularInline):
    """
    Inline class for the 'Author' model within 'BookAuthor' admin.

    Fields:
        - model: The model to be displayed inline.
        - fk_name: The foreign key to associate with.
        - extra: Number of empty forms to display for adding related objects.
    """
    model = BookAuthor
    fk_name = "author"
    extra = 1

###################### Book Admin ####################

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin class for the 'Book' model.

    Fields:
        - list_display: Display fields in the list view.
        - list_filter: Fields available for filtering.
        - search_fields: Fields available for searching.
        - list_display_links: Fields with links in the list view.
        - list_editable: Editable fields in the list view.
        - inlines: Inline models for the 'Book' admin.
    """
    list_display = ['ISBN', 'title', 'create_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['ISBN', 'title']
    list_display_links = ['ISBN', 'title']
    list_editable = ['is_active']
    inlines = [BookInline]

################## Book Shelf Admin ##################

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    """
    Admin class for the 'BookShelf' model.

    Fields:
        - list_display: Display fields in the list view.
        - search_fields: Fields available for searching.
        - list_display_links: Fields with links in the list view.
    """
    list_display = ['user', 'book', 'shelf']
    search_fields = ['user', 'book']
    list_display_links = ['user', 'book']

class ShelfInline(admin.TabularInline):
    """
    Inline class for the 'Shelf' model within 'BookShelf' admin.

    Fields:
        - model: The model to be displayed inline.
        - fk_name: The foreign key to associate with.
        - extra: Number of empty forms to display for adding related objects.
    """
    model = BookShelf
    fk_name = "shelf"
    extra = 1

class UserBookShelfInline(admin.TabularInline):
    """
    Inline class for the 'User' model within 'BookShelf' admin.

    Fields:
        - model: The model to be displayed inline.
        - fk_name: The foreign key to associate with.
        - extra: Number of empty forms to display for adding related objects.
    """
    model = BookShelf
    fk_name = "user"
    extra = 1

##################### Shelf Admin ####################

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    """
    Admin class for the 'Shelf' model.

    Fields:
        - list_display: Display fields in the list view.
        - list_filter: Fields available for filtering.
        - search_fields: Fields available for searching.
        - list_display_links: Fields with links in the list view.
        - inlines: Inline models for the 'Shelf' admin.
    """
    list_display = ['name', 'user']
    list_filter = ['user']
    search_fields = ['name', 'user']
    list_display_links = ['name']
    inlines = [ShelfInline]

########################## Tag #######################

class TagAdmin(admin.ModelAdmin):
    """
    Admin class for the 'Tag' model.
    """
    pass

admin.site.register(Tag, TagAdmin)
