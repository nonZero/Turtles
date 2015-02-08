"use strict";

window.addEventListener("map:init", function (e) {

    // Prevent the whole app from failing if we can't init the google maps
    // layer  for any reason.
    try {
        var googleLayer = new L.Google('HYBRID');
    } catch (e) {
        console.error("Error adding Google maps layer", e);
        return;
    }

    var map = (e.originalEvent ? e.originalEvent.detail : e.detail).map;

    // Disable the current active layer.
    var layers = map.layerscontrol._layers;
    for (var key in layers) {
        if (layers[key].overlay) {
            // Skip overlay layers
            continue;
        }
        if (map.hasLayer(layers[key].layer)) {
            map.removeLayer(layers[key].layer);
            break;
        }
    }

    // Add and enable the google maps layer
    map.layerscontrol.addBaseLayer(googleLayer, 'Google Satellite');
    map.addLayer(googleLayer);

}, false);
