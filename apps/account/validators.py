import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def user_validation(phone_number, password, *args, **kwargs):
    """
    Validate user information.
    """
    validation_functions = [
        {"name": validate_phone_number, "args": [phone_number]},
        {"name": validate_password, "args": [password]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_phone_number(phone_number: str):

    pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$"
    match = re.match(pattern, phone_number)
    if not match:
        raise ValidationError(_("Invalid phone number"))
    return True


def validate_password(password: str):

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

def auther_validation(first_name, last_name, *args, **kwargs):
    """
    Validate author information.
    """
    validation_functions = [
        {"name": validate_name, "args": [first_name]},
        {"name": validate_name, "args": [last_name]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_name(name: str):

    pattern = r'^[^0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|]*$'
    match = re.match(pattern, name)
    if not match:
        raise ValidationError(_(f"{name} should not started with numbers or contain symbolic char."))

    return True
