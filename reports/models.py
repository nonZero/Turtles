# coding: utf-8
import random
import string

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from reports.enums import TurtleAlive, TurtleLocation, TurtleSpecies, \
    TurtleBehaviour, TailLength


CHARS = string.lowercase + string.digits
UID_LENGTH = 12


def make_uid():
    return "".join([random.choice(CHARS) for x in xrange(UID_LENGTH)])


class TurtleReport(models.Model):
    observer = models.CharField(_('Observer'), max_length=50, db_index=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    date = models.DateField(_('Observation Date'), null=True, blank=True,
                            db_index=True)

    time = models.TimeField(_('Observation Time'), null=True, blank=True,
                            db_index=True)

    point_lat = models.FloatField(null=True, blank=True)
    point_lan = models.FloatField(null=True, blank=True)

    # point = models.PointField(null=True, blank=True, srid=settings.ITM_SRID,
    # verbose_name=_('point'))

    point_accuracy = models.FloatField(null=True, blank=True)

    alive = models.IntegerField(_('Turtle Status'),
                                choices=TurtleAlive.choices,
                                default=TurtleAlive.ALIVE)
    location = models.IntegerField(_('Turtle Place'),
                                   choices=TurtleLocation.choices,
                                   default=TurtleLocation.SHORE)
    species = models.IntegerField(_('Turtle Species'),
                                  choices=TurtleSpecies.choices,
                                  default=TurtleSpecies.DONT_KNOW)
    behaviour = models.IntegerField(_('Turtle Behaviour'),
                                    choices=TurtleBehaviour.choices,
                                    null=True, blank=True)
    tail_length = models.IntegerField(_('Tail Length'),
                                      choices=TailLength.choices,
                                      default=TailLength.UK)

    comment = models.TextField(
        _("Observation Description"), null=True, blank=True, help_text=
        _(
            'Anything else you want to tell us? Did the turtle have a tag on it?'))

    uid = models.CharField(max_length=UID_LENGTH, default=make_uid)

    def __unicode__(self):
        return u"[#{}] {} {}".format(self.id, self.observer, self.date or "?")

    class Meta:
        verbose_name = _("turtle report")
        verbose_name_plural = _("turtle reports")


class TurtleReportPhoto(models.Model):
    report = models.ForeignKey(TurtleReport, related_name="photos")
    from_email = models.EmailField(null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)
    img = models.ImageField(upload_to="reports")
    verified = models.BooleanField(default=False)
