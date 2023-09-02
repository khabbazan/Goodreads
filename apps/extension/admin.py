from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.extension.models import Image


class ImageInline(GenericTabularInline):
    model = Image
    extra = 1


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
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
