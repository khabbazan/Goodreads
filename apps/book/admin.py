from django.contrib import admin

from apps.book.models import Book

###################### Book Admin ####################

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['ISBN', 'title', 'create_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['ISBN', 'title']
    list_display_links = ['ISBN', 'title']
    list_editable = ['is_active']

