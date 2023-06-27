import pdb
import re
from django.utils.translation import gettext_lazy as _

def base_user_validation(phone_number, password, *args, **kwargs):
    validation_functions = [
        {"name": validate_phone_number, "args": [phone_number]},
        {"name": validate_password, "args": [password]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_phone_number(phone_number: str):

    pattern = r"^09[0-3,9]\d{8}$"
    match = re.match(pattern, phone_number)
    if not match:
        raise ValueError(_("Invalid phone number"))
    return True


def validate_password(password: str):

    len_ptr = re.compile(r'(\w{8,})')  # Check if password has at least 8 characters
    if not re.match(len_ptr, password):
        raise ValueError(_('Password must contain at least 8 characters'))

    lower_ptr = re.compile(r'[a-z]+')  # Check if at least one lowercase letter
    if not re.findall(lower_ptr, password):
        raise ValueError(_('Password must contain at least one lowercase character'))

    upper_ptr = re.compile(r'[A-Z]+')  # Check if at least one upper case letter
    if not re.findall(upper_ptr, password):
        raise ValueError(_('Password must contain at least one uppercase character'))

    digit_ptr = re.compile(r'[0-9]+')  # Check if at least one digit.
    if not re.findall(digit_ptr, password):
        raise ValueError(_('Password must contain at least one digit character'))

    return True


def staff_user_validation(is_staff, is_superuser, *args, **kwargs):
    validation_functions = [
        {"name": validate_staff_permissions, "args": [is_staff, is_superuser]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True

def validate_staff_permissions(is_staff: bool, is_superuser: bool):
    if is_staff is not True:
        raise ValueError(_("Superuser must have is_staff=True."))
    if is_superuser is not True:
        raise ValueError(_("Superuser must have is_superuser=True."))

    return True
