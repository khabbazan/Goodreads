from django.contrib import admin

from apps.account.models import User, Author, Relation
from apps.book.admin import AuthorInline, UserBookShelfInline

###################### Relation Admin ####################

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['followers', 'following']
    search_fields = ['followers', 'following']
    list_display_links = ['followers', 'following']

class FollowingInline(admin.TabularInline):
    model = Relation
    fk_name = "following"
    extra = 1

class FollowersInline(admin.TabularInline):
    model = Relation
    fk_name = "followers"
    extra = 1

###################### User Admin ####################

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'date_joined', 'is_staff', 'is_active', 'is_author']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['phone_number']
    list_display_links = ['phone_number']
    list_editable = ['is_staff', 'is_active', 'is_author']
    inlines = [FollowingInline, FollowersInline, UserBookShelfInline]

###################### Author Admin ####################

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'full_name']
    search_fields = ['phone_number']
    list_display_links = ['phone_number', 'full_name']
    inlines = [AuthorInline]

    def phone_number(self, x):
        return x.user.phone_number
