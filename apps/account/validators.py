import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def user_validation(phone_number=None, password=None, email=None, *args, **kwargs):
    """
    Validate user information.

    Args:
        phone_number (str): The user's phone number.
        password (str): The user's password.
        email (str): The user's email address.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    validation_functions = [
        {"name": validate_phone_number, "args": [phone_number]},
        {"name": validate_password, "args": [password]},
        {"name": validate_email, "args": [email]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_phone_number(phone_number: str):
    """
    Validate a phone number.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    if phone_number is not None:
        pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$"
        match = re.match(pattern, phone_number)
        if not match:
            raise ValidationError(_("Invalid phone number"))
        return True

def validate_password(password: str):
    """
    Validate a password.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    if password is not None:
        len_ptr = re.compile(r'(\w{8,})')  # Check if password has at least 8 characters
        if not re.match(len_ptr, password):
            raise ValidationError(_('Password must contain at least 8 characters'))

        lower_ptr = re.compile(r'[a-z]+')  # Check if at least one lowercase letter
        if not re.findall(lower_ptr, password):
            raise ValidationError(_('Password must contain at least one lowercase character'))

        upper_ptr = re.compile(r'[A-Z]+')  # Check if at least one upper case letter
        if not re.findall(upper_ptr, password):
            raise ValidationError(_('Password must contain at least one uppercase character'))

        digit_ptr = re.compile(r'[0-9]+')  # Check if at least one digit.
        if not re.findall(digit_ptr, password):
            raise ValidationError(_('Password must contain at least one digit character'))

        return True

def validate_email(email: str):
    """
    Validate email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    if email is not None:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        match = re.match(pattern, email)
        if not match:
            raise ValidationError(_("Invalid email address"))
        return True

def author_validation(first_name=None, last_name=None, *args, **kwargs):
    """
    Validate author information.

    Args:
        first_name (str): The author's first name.
        last_name (str): The author's last name.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    validation_functions = [
        {"name": validate_name, "args": [first_name]},
        {"name": validate_name, "args": [last_name]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_name(name: str):
    """
    Validate a name.

    Args:
        name (str): The name to validate.

    Returns:
        bool: True if validation succeeds.

    Raises:
        ValidationError: If validation fails.
    """
    if name is not None:
        pattern = r'^[^0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|]*$'
        match = re.match(pattern, name)
        if not match:
            raise ValidationError(_(f"{name} should not start with numbers or contain symbolic characters."))

        return True
