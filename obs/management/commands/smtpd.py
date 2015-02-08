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
            print add_email(sender, to, subject, text, html, images)


        inbox = Inbox(on_message, 4467, '127.0.0.1')
        inbox.serve()
