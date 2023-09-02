import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def book_validation(ISBN=None, title=None, description=None, *args, **kwargs):
    """
    Validate user information.
    """
    validation_functions = [
        {"name": validate_ISBN, "args": [ISBN]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_ISBN(ISBN: str):

    if ISBN is not None:
        pattern = r'^[0-9]{9}([0-9]|X)$'
        match = re.match(pattern, ISBN)
        if not match:
            raise ValidationError(_("Invalid ISBN"))
        return True
