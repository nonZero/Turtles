"use strict";

var get_location_promise = function () {
    var deferred = $.Deferred();
    navigator.geolocation.getCurrentPosition(
        deferred.resolve,
        deferred.reject,
        {
            enabaleHighAccuracy: true,
            maximumAge: 0
        }
    );
    return deferred.promise();
};

var get_map_promise = function () {
    var deferred = $.Deferred();

    $(window).on("map:init", function (e) {
        var map = (e.originalEvent ? e.originalEvent.detail : e.detail).map;
        deferred.resolve(map);
    });

    return deferred.promise();
};


$(function () {
    var has_gps;

    has_gps = !!navigator.geolocation;

    if (has_gps) {
        $.when(get_map_promise(), get_location_promise()).done(function (map, position) {
            var latlng = L.latLng(position.coords.latitude, position.coords.longitude);
            console.log(latlng, position);
            var circle = L.circle(latlng, position.coords.accuracy).addTo(map);
            map.setView(latlng, map.getMaxZoom());
        });
    }

});