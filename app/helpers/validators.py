import os
from django.core.exceptions import ValidationError


def extension_validation(value, valid_extensions):
    extension_string = ', '.join(valid_extensions)
    exception_message = f'File type should be {extension_string}'

    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError(exception_message)


def validate_xlsx_file_extension(value):
    extensions = ['.xlsx']
    extension_validation(value, extensions)

