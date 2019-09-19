from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def image_restriction(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width >= 500 or image_height >= 500:
        raise ValidationError('The image needs to be less than 500x500.')
