from django.conf import settings
from django.core.management.base import BaseCommand

from inbox import Inbox
from email_parser import parse_message
from obs.incoming import add_email


class Command(BaseCommand):
    help = "Observations smtpd."

    def handle(self, *args, **options):
        def on_message(to, sender, subject, body):
            # fn = "mymsg_{}.txt".format(get_random_string(5))
            # with open(fn, "wb") as f:
            # f.write(body)
            # print "written {} bytes to {}.".format(len(body), fn)
            text, html, images = parse_message(body)
            msg = add_email(sender, to, subject, text, html, images)
            # TODO: send confirmation email
            # TODO: send email to managers


        inbox = Inbox(on_message, settings.TURTLES_SMTP_PORT,
                      settings.TURTLES_SMTP_HOST)
        inbox.serve()
