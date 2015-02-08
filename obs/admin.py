# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from . import models


class TurtleObservationEmailInline(admin.TabularInline):
    model = models.TurtleObservationEmail


class TurtleObservationPhotoInline(admin.TabularInline):
    model = models.TurtleObservationPhoto


class TurleObservationAdmin(admin.ModelAdmin):
    inlines = [
        TurtleObservationEmailInline,
        TurtleObservationPhotoInline,
    ]
    list_display = (
        '__unicode__',
        'created_at',
        'email_count',
        'photo_count',
    )

    def email_count(self, obj):
        return obj.emails.count()

    def photo_count(self, obj):
        return obj.photos.count()


admin.site.register(models.TurtleObservation, TurleObservationAdmin)