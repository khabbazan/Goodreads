from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from apps.extension.models import Image

class ImageInline(GenericTabularInline):
    """
    Inline admin class for the 'Image' model.

    Fields:
        model (Image): The model associated with this inline.
        extra (int): The number of empty forms to display for adding new images.
    """
    model = Image
    extra = 1

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin class for the 'Image' model.

    Fields:
        fieldsets (list of tuple): A list of fieldset definitions for organizing form fields.
    """
    fieldsets = [
        (
            "Basic options",
            {
                "fields": ["original_image", "user", "content_type", "object_id"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["large_image", "medium_image", "small_image"],
            },
        ),
    ]
