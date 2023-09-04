from django.contrib import admin

from apps.account.models import User, Author, Relation
from apps.book.admin import AuthorInline, UserBookShelfInline
from apps.extension.admin import ImageInline

###################### Relation Admin ####################

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
    search_fields = ['follower', 'following']
    list_display_links = ['follower', 'following']

class FollowingInline(admin.TabularInline):
    model = Relation
    fk_name = "following"
    extra = 1

class FollowersInline(admin.TabularInline):
    model = Relation
    fk_name = "follower"
    extra = 1

###################### User Admin ####################

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'date_joined', 'is_staff', 'is_active', 'is_author']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['phone_number']
    list_display_links = ['phone_number']
    list_editable = ['is_staff', 'is_active', 'is_author']
    inlines = [ImageInline, FollowingInline, FollowersInline, UserBookShelfInline]

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()

###################### Author Admin ####################

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'full_name']
    search_fields = ['phone_number']
    list_display_links = ['phone_number', 'full_name']
    inlines = [AuthorInline]

    def phone_number(self, x):
        return x.user.phone_number
