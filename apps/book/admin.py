from django.contrib import admin

from apps.book.models import Book, BookAuthor

###################### Relation Admin ####################
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
