from django.contrib import admin

from apps.account.models import User, Author, Relation
from apps.book.admin import AuthorInline, UserBookShelfInline
from apps.extension.admin import ImageInline

###################### Relation Admin ####################

class RelationAdmin(admin.ModelAdmin):
    """
    Admin class for managing the 'Relation' model.

    Fields:
        list_display (list): Fields to display in the list view.
        search_fields (list): Fields to search in the admin interface.
        list_display_links (list): Fields in the list view that are linked to detail views.
    """

    list_display = ['follower', 'following']
    search_fields = ['follower', 'following']
    list_display_links = ['follower', 'following']

class FollowingInline(admin.TabularInline):
    """
    Tabular inline admin class for managing 'Relation' instances where the model is 'following'.

    Fields:
        model (Model): The related model for the inline.
        fk_name (str): The foreign key attribute name.
        extra (int): Number of extra forms to display.
    """

    model = Relation
    fk_name = "following"
    extra = 1

class FollowersInline(admin.TabularInline):
    """
    Tabular inline admin class for managing 'Relation' instances where the model is 'follower'.

    Fields:
        model (Model): The related model for the inline.
        fk_name (str): The foreign key attribute name.
        extra (int): Number of extra forms to display.
    """

    model = Relation
    fk_name = "follower"
    extra = 1

###################### User Admin ####################

class UserAdmin(admin.ModelAdmin):
    """
    Admin class for managing the 'User' model.

    Fields:
        list_display (list): Fields to display in the list view.
        list_filter (list): Fields to filter the list view by.
        search_fields (list): Fields to search in the admin interface.
        list_display_links (list): Fields in the list view that are linked to detail views.
        list_editable (list): Fields that can be edited directly in the list view.
        inlines (list): Inline classes to include in the admin interface.
    """

    list_display = ['phone_number', 'date_joined', 'is_staff', 'is_active', 'is_author']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['phone_number']
    list_display_links = ['phone_number']
    list_editable = ['is_staff', 'is_active', 'is_author']
    inlines = [ImageInline, FollowingInline, FollowersInline, UserBookShelfInline]

    def save_model(self, request, obj, form, change):
        """
        Custom method to save a model instance to the database.

        Args:
            request: The current request.
            obj: The model instance to be saved.
            form: The form used for saving the instance.
            change (bool): Indicates whether the instance is being edited.

        Returns:
            None
        """
        obj.save()

###################### Author Admin ####################

class AuthorAdmin(admin.ModelAdmin):
    """
    Admin class for managing the 'Author' model.

    Fields:
        list_display (list): Fields to display in the list view.
        search_fields (list): Fields to search in the admin interface.
        list_display_links (list): Fields in the list view that are linked to detail views.
        inlines (list): Inline classes to include in the admin interface.
    """

    list_display = ['phone_number', 'full_name']
    search_fields = ['phone_number']
    list_display_links = ['phone_number', 'full_name']
    inlines = [AuthorInline]

    def phone_number(self, x):
        """
        Custom method to retrieve the phone number associated with the user.

        Args:
            x: The Author instance.

        Returns:
            str: The phone number of the associated user.
        """
        return x.user.phone_number
