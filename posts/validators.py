from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions



def image_filed_validator(value):
    width, height = get_image_dimensions(value)
    if width != 200 or height != 200:
        raise ValidationError(f"You need to upload an image with {200}x{200} dimensions")
    return value



