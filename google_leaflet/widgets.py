from leaflet.forms.widgets import LeafletWidget


class GoogleLeafletWidget(LeafletWidget):
    @property
    def media(self):
        m = super(GoogleLeafletWidget, self).media
        m.add_js((
            'google_leaflet/Google.js',
            'google_leaflet/google-leaflet.js',
            'http://maps.google.com/maps/api/js?v=3.2&sensor=false',
        ))
        return m
