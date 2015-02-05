from django.contrib import admin
from reports.models import TurtleReport, TurtleReportPhoto


class TurtleReportPhotoInline(admin.TabularInline):
    model = TurtleReportPhoto


class TurleReportAdmin(admin.ModelAdmin):
    inlines = [
        TurtleReportPhotoInline
    ]
    list_display = (
        '__unicode__',
        'created_at',
    )

admin.site.register(TurtleReport, TurleReportAdmin)