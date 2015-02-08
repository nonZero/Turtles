# coding: utf-8
from __future__ import unicode_literals

import floppyforms.__future__ as forms
from leaflet.forms.widgets import LeafletWidget
from django.utils.translation import ugettext_lazy as _
from google_leaflet.widgets import GoogleLeafletWidget

from obs.models import TurtleObservation, TurtleObservationPhoto


class ObservationForm(forms.ModelForm):
    class Meta:
        model = TurtleObservation
        exclude = (
            'uid',
            'email_uid',
        )
        widgets = {
            'point': GoogleLeafletWidget(),
            'point_accuracy': forms.HiddenInput(),
        }
        labels = {
            'observer': _("Your Name"),
            'email': _("Your Email"),
            'phone': _("Your Phone"),
        }
    class Media:
        js = (
            'js/turtleobservation_form.js',
        )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = TurtleObservationPhoto
        fields = (
            'img',
        )

