# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


class TailLength(object):
    UK = 0
    LONG = 1
    SHORT = 2
    choices = (
        (UK, _('Unknown')),
        (LONG, _('Long')),
        (SHORT, _('Short')),
    )


class TurtleAlive(object):
    DONT_KNOW = 4
    # NOT_SURE = 3
    INJURED = 2
    ALIVE = 1
    DEAD = 0

    choices = (
        (DONT_KNOW, _('Unknown')),
        # (NOT_SURE, _('''I'm not sure''')),
        (INJURED, _('Injured Turtle')),
        (ALIVE, _('Live Turtle')),
        (DEAD, _('Dead Turtle')),
    )


class TurtleLocation(object):
    SHORE = 1
    DEPTH0 = 2
    DEPTH5 = 3
    BOTTOM = 4

    choices = (
        (SHORE, _('On the shore')),
        (DEPTH0, _('At Sea level, less than 5m deep')),
        (DEPTH5, _('Deeper than 5m deep')),
        (BOTTOM, _('On the Sea bottom')),
    )


class TurtleSpecies(object):
    MYDAS = 1
    CARETTA = 2
    DONT_KNOW = 3
    ERETMOCHELYS = 4
    DERMOCHELYS = 5
    SOFT = 6
    SWAMP = 7

    choices = (
        (DONT_KNOW, _('Unknown')),
        (MYDAS, _('Chelonia mydas, Green Sea Turtle')),
        (CARETTA, _('Carette caretta, Loggerhead Sea Turtle')),
        (ERETMOCHELYS, _('Eretmochelys imbricata, Hawksbill Sea Turtle')),
        (DERMOCHELYS, _('Dermochelys coriacea, Leatherback Sea Turtle')),
        (SOFT, _('Trionyx triunguis, Nile Soft Shell Turtle')),
        (SWAMP, _('Mauremys caspica, Caspian Turtle')),
    )


class TurtleBehaviour(object):
    BREETHING = 1
    BREEDING = 2
    FEEDING = 3
    NESTING = 4
    SLEEPING = 5
    SWIMMING = 6
    ELSE = 7

    choices = (
        (BREETHING, _('Breathing')),
        (BREEDING, _('Breeding')),
        (FEEDING, _('Feeding')),
        (NESTING, _('Nesting')),
        (SLEEPING, _('Sleeping')),
        (SWIMMING, _('Swimming')),
        (ELSE, _('Other')),
    )

