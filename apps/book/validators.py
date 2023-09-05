import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def book_validation(ISBN=None, title=None, description=None, *args, **kwargs):
    """
    Validate book information.

    Args:
        ISBN (str): The International Standard Book Number to validate.
        title (str): The title of the book to validate.
        description (str): The description of the book to validate.
        *args: Additional positional arguments (unused).
        **kwargs: Additional keyword arguments (unused).

    Returns:
        bool: True if validation succeeds, False otherwise.
    """
    validation_functions = [
        {"name": validate_ISBN, "args": [ISBN]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_ISBN(ISBN: str):
    """
    Validate the International Standard Book Number (ISBN).

    Args:
        ISBN (str): The ISBN to validate.

    Raises:
        ValidationError: If the ISBN is invalid.

    Returns:
        bool: True if the ISBN is valid, False otherwise.
    """
    if ISBN is not None:
        pattern = r'^[0-9]{9}([0-9]|X)$'
        match = re.match(pattern, ISBN)
        if not match:
            raise ValidationError(_("Invalid ISBN"))
        return True
