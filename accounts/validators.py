import os.path

from django.core.exceptions import ValidationError
def allow_only_image_validator(value):
    ext = os.path.splitext(value.name)[-1]
    image_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in image_extensions:
        raise ValidationError("Unsupported file extensions. Allowed extensions are " + str(image_extensions))