from django.db import models
from django.utils.translation import gettext_lazy as _


######################### Book #######################

class Book(models.Model):

    ISBN = models.CharField(_("ISBN"), max_length=100, unique=True)
    title = models.CharField(_("book title"), max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title



