import os
import uuid
import base64
from io import BytesIO
from PIL import Image as PilImage

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _

from helpers.temp_generator import generate_random_filename

class Image(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=generate_random_filename)
    large_image = models.ImageField(null=True, blank=True, upload_to='images/')
    medium_image = models.ImageField(null=True, blank=True, upload_to='images/')
    small_image = models.ImageField(null=True, blank=True, upload_to='images/')

    create_date = models.DateField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        if settings.DEBUG:
            return self.original_image.file.name
        return self.original_image.url

    def delete(self, *args, **kwargs):

        'self.original_image.file.name'

        if self.original_image and default_storage.exists(str(self.original_image)):
            default_storage.delete(str(self.original_image))

        if self.large_image and default_storage.exists(str(self.large_image)):
            default_storage.delete(str(self.large_image))

        if self.medium_image and default_storage.exists(str(self.medium_image)):
            default_storage.delete(str(self.medium_image))

        if self.small_image and default_storage.exists(str(self.small_image)):
            default_storage.delete(str(self.small_image))

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        super().save()
        img = PilImage.open(self.original_image)

        # Resize image for small size
        small_size = settings.IMAGE_SIZE.get("small", (100, 100))
        small_img = img.copy()
        small_img.thumbnail(small_size)
        small_img_io = BytesIO()
        small_img_file = InMemoryUploadedFile(small_img_io, None, f"{self.original_image.name.split('.')[:-1]}_small.png", "image/png", small_img_io.tell(), None)
        self.small_image = small_img_file

        # Resize image for medium size
        medium_size = settings.IMAGE_SIZE.get("medium", (300, 300))
        medium_img = img.copy()
        medium_img.thumbnail(medium_size)
        medium_img_io = BytesIO()
        medium_img_file = InMemoryUploadedFile(medium_img_io, None, f"{self.original_image.name.split('.')[:-1]}_medium.png", "image/png", medium_img_io.tell(), None)
        self.medium_image = medium_img_file

        # Resize image for large size
        large_size = settings.IMAGE_SIZE.get("large", (800, 800))
        large_img = img.copy()
        large_img.thumbnail(large_size)
        large_img_io = BytesIO()
        large_img_file = InMemoryUploadedFile(large_img_io, None, f"{self.original_image.name.split('.')[:-1]}_large.png", "image/png", large_img_io.tell(), None)
        self.large_image = large_img_file

        super().save(*args, **kwargs)

    @staticmethod
    def base64_to_image(base64_string):
        if not base64_string:
            return None

        img_format, img_str = base64_string.split(";base64,")
        ext = img_format.split("/")[-1]
        image_content = ContentFile(base64.b64decode(img_str), name=f'tmp_avatar.{ext}')

        return image_content

