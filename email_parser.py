import email
import email.message

from django.core.files.images import ImageFile
from django.core.files.base import ContentFile


class ImageContentFile(ContentFile, ImageFile):
    pass


def parse_part(part):
    return part.get_payload(decode=True).decode(
        part.get_content_charset() or "ascii")


def parse_message(body):
    """Parses an email message body.
     returns (text, html, [ImageFile...])"""

    msg = email.message_from_string(body)
    text = None
    html = None
    images = []
    for m in msg.walk():
        ct = m.get_content_type()
        if ct == "text/plain":
            if not text:
                text = parse_part(m)
        elif ct == "text/html":
            if not html:
                html = parse_part(m)
        elif ct.startswith("image/"):
            f = ImageContentFile(m.get_payload(decode=True), m.get_filename())
            if f._get_image_dimensions():
                # Image is valid
                images.append(f)
    return text, html, images
