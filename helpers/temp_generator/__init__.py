import os
import tempfile
import uuid
from datetime import datetime

from django.utils.translation import gettext_lazy as _


def generate_temp_file(with_datetime=True):
    """
    Generate file in tmp directory.
    """
    suff = ""
    if with_datetime:
        suff = f'-{datetime.now().strftime("%Y%m%d_%H%M%S")}'

    tf = tempfile.NamedTemporaryFile(suffix=suff)

    return tf.name


def generate_random_filename(instance=None, filename=None, ext=None, suffix="", with_datetime=False, directory="images"):
    """Generate a unique filename for the uploaded image."""
    if filename is None and ext is None:
        return ValueError(_("You should provide filename or ext."))

    ext = filename.split(".")[-1] if ext is None else ext

    filename = f'{uuid.uuid4()}'
    filename = f'{suffix}-{filename}' if suffix else filename
    filename = f'{filename}-{datetime.now().strftime("%Y%m%d_%H%M%S")}' if with_datetime else filename

    filename = f'{filename}.{ext}'

    return os.path.join(directory, filename)
