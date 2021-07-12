from django.core.exceptions import ValidationError


def file_size_validator(field):
    if field.size < 10**7:
        return field
    else:
        raise ValidationError("max size 10MB")
