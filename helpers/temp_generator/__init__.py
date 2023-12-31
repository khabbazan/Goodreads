import os
import tempfile
import uuid
from datetime import datetime

from django.utils.translation import gettext_lazy as _


def generate_temp_file(with_datetime=True):
    """
    Generate a temporary file in the system's temporary directory.

    Args:
        with_datetime (bool): Whether to include a timestamp in the temporary file's name.

    Returns:
        str: The path to the generated temporary file.
    """
    suff = ""
    if with_datetime:
        suff = f'-{datetime.now().strftime("%Y%m%d_%H%M%S")}'

    tf = tempfile.NamedTemporaryFile(suffix=suff)

    return tf.name


def generate_random_filename(instance=None, filename=None, ext=None, suffix="", with_datetime=False, directory="images"):
    """
    Generate a unique filename for an uploaded file.

    Args:
        instance: The instance associated with the uploaded file (unused in this function).
        filename (str): The original filename or None.
        ext (str): The file extension or None.
        suffix (str): An optional suffix to append to the generated filename.
        with_datetime (bool): Whether to include a timestamp in the filename.
        directory (str): The directory where the file will be stored.

    Returns:
        str: The generated unique filename.

    Raises:
        ValueError: If both filename and ext are None.
    """
    if filename is None and ext is None:
        raise ValueError(_("You should provide filename or ext."))

    ext = filename.split(".")[-1] if ext is None else ext

    filename = f"{uuid.uuid4()}"
    filename = f"{suffix}-{filename}" if suffix else filename
    filename = f'{filename}-{datetime.now().strftime("%Y%m%d_%H%M%S")}' if with_datetime else filename

    filename = f"{filename}.{ext}"

    return os.path.join(directory, filename)
