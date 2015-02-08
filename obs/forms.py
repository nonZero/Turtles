# coding: utf-8
from __future__ import unicode_literals

import floppyforms as forms

from obs.models import TurtleObservation, TurtleObservationPhoto


class ObservationForm(forms.ModelForm):
    class Meta:
        model = TurtleObservation
        exclude = (
            'uid',
        )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = TurtleObservationPhoto
        fields = (
            'img',
        )

