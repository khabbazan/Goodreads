from django.contrib import admin

from apps.book.models import Book
from apps.book.models import BookAuthor
from apps.book.models import Shelf
from apps.book.models import BookShelf
from apps.book.models import Tag

###################### BookAuthor Admin ####################
@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['book', 'author']
    search_fields = ['book', 'author']
    list_display_links = ['book', 'author']

class BookInline(admin.TabularInline):
    model = BookAuthor
    fk_name = "book"
    extra = 1

class AuthorInline(admin.TabularInline):
    model = BookAuthor
    fk_name = "author"
    extra = 1

###################### Book Admin ####################

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['ISBN', 'title', 'create_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['ISBN', 'title']
    list_display_links = ['ISBN', 'title']
    list_editable = ['is_active']
    inlines = [BookInline]

################## Book Shelf Admin ##################

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'shelf']
    search_fields = ['user', 'book']
    list_display_links = ['user', 'book']

class ShelfInline(admin.TabularInline):
    model = BookShelf
    fk_name = "shelf"
    extra = 1

class UserBookShelfInline(admin.TabularInline):
    model = BookShelf
    fk_name = "user"
    extra = 1


##################### Shelf Admin ####################

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['user']
    search_fields = ['name', 'user']
    list_display_links = ['name']
    inlines = [ShelfInline]

########################## Tag #######################

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
