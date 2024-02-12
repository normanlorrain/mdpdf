import fitz
from . import log


def get_image_size(fname):
    image=fitz.Pixmap(fname)
    log.debug(f"get_image_size: {image.width}, {image.height}")
    return image.width, image.height

