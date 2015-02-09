# -*- coding: utf-8 -*-
from email.header import decode_header
import logging

import smtpd
import asyncore
import argparse
from email.parser import Parser


logger = logging.getLogger(__name__)


class InboxServer(smtpd.SMTPServer, object):
    """Logging-enabled SMTPServer instance with handler support."""

    def __init__(self, handler, *args, **kwargs):
        super(InboxServer, self).__init__(*args, **kwargs)
        self._handler = handler

    def process_message(self, peer, mailfrom, rcpttos, data):
        logger.info('Collating message from {0}'.format(mailfrom))
        msg = Parser().parsestr(data)
        subject = decode_header(msg['subject'])[0][0]
        logger.debug(
            dict(to=rcpttos, sender=mailfrom, subject=subject, body=data))
        try:
            return self._handler(to=rcpttos, sender=mailfrom, subject=subject,
                                 body=data)
        except:
            logger.error("Error handling email", exc_info=True)
            raise


class Inbox(object):
    """A simple SMTP Inbox."""

    def __init__(self, collator, port=None, address=None):
        self.collator = collator
        self.port = port
        self.address = address

    def serve(self, port=None, address=None):
        """Serves the SMTP server on the given port and address."""
        port = port or self.port
        address = address or self.address

        logger.info('Starting SMTP server at {0}:{1}'.format(address, port))

        server = InboxServer(self.collator, (address, port), None)

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            logger.info('Cleaning up')
