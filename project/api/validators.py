import os

from django.core.exceptions import ValidationError


def validate_upload_file(value):
    extension = os.path.splitext(value.name)[1].lower()
    if extension != '.xlsx':
        raise ValidationError('Unsupported file extension.')
