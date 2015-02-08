# coding: utf-8
from __future__ import unicode_literals
import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from . import enums


UID_LENGTH = 12
EMAIL_UID_LENGTH = 6
LETTERS = 'acefghjkmqrstuvwxyz'
DIGITS = '23456789'


def make_uid():
    return get_random_string(UID_LENGTH)


def make_email_uid():
    return get_random_string(3, LETTERS) + get_random_string(3, DIGITS)


class TurtleObservation(models.Model):
    observer = models.CharField(_('Observer'), max_length=50, db_index=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    date = models.DateField(_('Observation Date'), null=True, blank=True,
                            db_index=True, default=datetime.date.today)

    time = models.TimeField(_('Observation Time'), null=True, blank=True,
                            db_index=True)

    point = models.PointField(null=True, blank=True, srid=settings.ITM_SRID,
                              verbose_name=_('point'))

    point_accuracy = models.FloatField(null=True, blank=True)

    alive = models.IntegerField(_('Turtle Status'),
                                choices=enums.TurtleAlive.choices,
                                default=enums.TurtleAlive.ALIVE)
    location = models.IntegerField(_('Turtle Place'),
                                   choices=enums.TurtleLocation.choices,
                                   default=enums.TurtleLocation.SHORE)
    species = models.IntegerField(_('Turtle Species'),
                                  choices=enums.TurtleSpecies.choices,
                                  default=enums.TurtleSpecies.DONT_KNOW)
    behaviour = models.IntegerField(_('Turtle Behaviour'),
                                    choices=enums.TurtleBehaviour.choices,
                                    null=True, blank=True)
    tail_length = models.IntegerField(_('Tail Length'),
                                      choices=enums.TailLength.choices,
                                      default=enums.TailLength.UK)

    comment = models.TextField(
        _("Observation Description"), null=True, blank=True, help_text=
        _(
            'Anything else you want to tell us? Did the turtle have a tag on it?'))

    uid = models.CharField(max_length=UID_LENGTH, default=make_uid)
    email_uid = models.CharField(max_length=EMAIL_UID_LENGTH,
                                 default=make_email_uid)

    class Meta:
        verbose_name = _("turtle observation")
        verbose_name_plural = _("turtle observations")

    def __unicode__(self):
        return u"[#{}] {} {}".format(self.id, self.observer, self.date or "?")

    def get_absolute_url(self):
        return reverse('ob', args=(self.uid,))

    def incoming_email(self):
        return "{}{}@{}".format(
            settings.TURTLE_MAIL_PREFIX,
            self.email_uid,
            settings.TURTLE_SMTP_DOMAIN,
        )

    def uploads(self):
        return self.photos.filter(email=None)


class TurtleObservationEmail(models.Model):
    ob = models.ForeignKey(TurtleObservation, related_name="emails")
    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    sender = models.EmailField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    body_text = models.EmailField(null=True, blank=True)
    body_html = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("turtle observation email")
        verbose_name_plural = _("turtle observation emails")

    def __unicode__(self):
        return u"[#{}.{}] {} {}".format(self.ob.id, self.id, self.sender,
                                        self.created_at)


class TurtleObservationPhoto(models.Model):
    ob = models.ForeignKey(TurtleObservation, related_name="photos")
    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    email = models.ForeignKey(TurtleObservationEmail, null=True, blank=True,
                              related_name='photos')
    img = models.ImageField(upload_to="reports", width_field='width',
                            height_field='height')
    width = models.IntegerField()
    height = models.IntegerField()
    original_filename = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _("turtle observation photo")
        verbose_name_plural = _("turtle observation photos")

    def __unicode__(self):
        return u"[#{}.{}] {}x{} {}".format(self.ob.id, self.id, self.width,
                                           self.height,
                                           self.created_at)
