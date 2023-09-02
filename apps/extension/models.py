import os
import uuid
from io import BytesIO
from PIL import Image as PilImage

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.account.models import User

def upload_to_uuid(instance, filename):
    """Generate a unique filename for the uploaded image."""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("images/", filename)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=upload_to_uuid)
    large_image = models.ImageField(null=True, blank=True)
    medium_image = models.ImageField(null=True, blank=True)
    small_image = models.ImageField(null=True, blank=True)

    create_date = models.DateField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.original_image.url

    def delete(self, *args, **kwargs):
        os.remove(str(settings.MEDIA_ROOT) + self.image.url)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        super().save()
        img = PilImage.open(self.original_image)

        # Resize image for small size
        small_size = settings.IMAGE_SIZE.get("small", (100, 100))
        small_img = img.copy()
        small_img.thumbnail(small_size)
        small_img_io = BytesIO()
        small_img.save(small_img_io, format="PNG")
        small_img_file = InMemoryUploadedFile(small_img_io, None, f"{self.original_image.name.split('.')[:-1]}_small.png", "image/png", small_img_io.tell(), None)
        self.small_image = small_img_file

        # Resize image for medium size
        medium_size = settings.IMAGE_SIZE.get("medium", (300, 300))
        medium_img = img.copy()
        medium_img.thumbnail(medium_size)
        medium_img_io = BytesIO()
        medium_img.save(medium_img_io, format="PNG")
        medium_img_file = InMemoryUploadedFile(medium_img_io, None, f"{self.original_image.name.split('.')[:-1]}_medium.png", "image/png", medium_img_io.tell(), None)
        self.medium_image = medium_img_file

        # Resize image for large size
        large_size = settings.IMAGE_SIZE.get("large", (800, 800))
        large_img = img.copy()
        large_img.thumbnail(large_size)
        large_img_io = BytesIO()
        large_img.save(large_img_io, format="PNG")
        large_img_file = InMemoryUploadedFile(large_img_io, None, f"{self.original_image.name.split('.')[:-1]}_large.png", "image/png", large_img_io.tell(), None)
        self.large_image = large_img_file

        super().save(*args, **kwargs)
