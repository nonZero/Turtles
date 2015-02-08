from leaflet.admin import LeafletGeoAdmin

from google_leaflet.widgets import GoogleLeafletWidget


class GoogleLeafletGeoAdmin(LeafletGeoAdmin):
    widget = GoogleLeafletWidget
