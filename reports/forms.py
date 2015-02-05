import floppyforms as forms

from reports.models import TurtleReport, TurtleReportPhoto


class ReportForm(forms.ModelForm):
    class Meta:
        model = TurtleReport
        exclude = (
            'uid',
        )


class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = TurtleReportPhoto
        fields = (
            'img',
        )

