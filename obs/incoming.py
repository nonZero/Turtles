from email.utils import parseaddr
import logging

from django.conf import settings

from obs.models import TurtleObservation

logger = logging.getLogger(__name__)


def find_uid(prefix, tos, our_domain=settings.TURTLE_SMTP_DOMAIN):
    for s in tos:
        name, email = parseaddr(s)
        if not email:
            continue
        box, domain = email.lower().split("@")
        if domain != our_domain.lower():
            continue
        if box.startswith(prefix.lower()):
            return box[len(prefix):]
    return None


def add_email(sender, tos, subject, text, html, images):
    uid = find_uid(settings.TURTLE_MAIL_PREFIX, tos)
    if not uid:
        logger.info("Received email with no uid: {}".format(tos))
        return None
    logger.info("Received email with uid {} from {}".format(uid, sender))
    try:
        ob = TurtleObservation.objects.get(email_uid=uid)
    except TurtleObservation.DoesNotExist:
        return None

    msg = ob.emails.create(
        sender=sender,
        subject=subject,
        body_text=text,
        body_html=html,
    )
    logger.info("Created email #{} for ob #{}".format(msg.id, ob.id))

    for img in images:
        o = ob.photos.create(
            email=msg,
            img=img,
            original_filename=img.name,
        )
        logger.info("Created image #{} for ob #{}".format(o.id, ob.id))

    return msg