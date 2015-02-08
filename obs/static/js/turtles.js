var $map = null;
var $gps_marker = null;
var $map_g_field = null;
var RedIcon = L.Icon.Default.extend({
                                            options: {
                                                iconUrl: '/static/images/marker-icon-red.png'
                                            }
                                        });
var redIcon = new RedIcon();
var geodjango_point = {};
    geodjango_point.fieldid = 'id_point';
    geodjango_point.modifiable = true;
    geodjango_point.geom_type = 'Point';
    geodjango_point.srid = 4326;

function id_point_map_callback(map, options) {
    $map = map;
    geodjango_point.store_class = L.FieldStore;
    $map_g_field = new L.GeometryField(geodjango_point);
    $map_g_field.addTo(map);

    if ($map.tap)
        $map.tap.disable();
        // enable tapping on touch screen
}

function detectGeoLocation() {
    if (navigator.geolocation)
        watchID = navigator.geolocation.watchPosition(
            update_long_lang,
            handleError,
            {
                enabaleHighAccuracy: true,
                maximumAge: 0,
                timeout: 60000
                // timeout is 60 seconds
            }
        );
    else {
        alert(gettext('Sorry, your browser does not support geolocation!'));
    }
}

function stopGeoLocation() {
    navigator.geolocation.clearWatch(watchID);
    if ($gps_marker) {
        $map.removeLayer($gps_marker);
        $gps_marker = null;
    }
    // accuracy == -1 when point is not via GPS
    document.getElementById('id_gps_accuracy').value = -1.0;
}

function updateGPSMarkerOnMap(point) {
    if ($gps_marker) {
        $gps_marker.setLatLng(point);
        $gps_marker.update();
    }
    else {
        $gps_marker = L.marker(point, {
                                        'draggable': false,
                                        'title': 'GPS Point',
                                        'alt': 'gps Point',
                                        'icon': redIcon
                                    }).addTo($map);
        $map.setView(point, 14);
    }
}

function gpsSwitchReverseDisplay() {
    $('.gps-switch-btn').toggleClass('active');
    $('.gps-switch-btn').toggleClass('btn-primary');
    $('.gps-switch-btn').toggleClass('btn-default');
}

function updateDateTime() {
    // using a trick to easily update data inside the input text box
    // by manipulating the pickers
    $('#id_obsr_date').focus();
    $('#id_obsr_time').focus();
    $('#id_obsr_time').blur();
}

function fixImageBtn() {
    var btn = '<button type="button" class="btn btn-info" id="upload_img">' + gettext("Upload Image") + '...</button>';
    $('#id_image').attr('accept', 'image/*');
    $('.field-image').prepend(btn);
}

/*
 *  an attempt to handle Android/Galaxy html5 image upload BUG
 *  by letting the user one try of uploading the image,
 *  in case of failure it will alert the user once, and then
 *  the image widget will be hidden from him
 */
function checkImageUploadIssue() {
    if (localStorage['new_obsr_image_problem'] == 'true') {
        if (!(localStorage['new_obsr_image_msg'] == 'true')) {
            localStorage['new_obsr_image_msg'] = 'true';
            // a flag to make sure alert will show only once
            alert(gettext("We are sorry, but it seems that your device doesn't support HTML5 image upload"));
        }
        $('[for="id_image"]').hide();
        localStorage['new_obsr_image_problem_verified'] = 'true';
        // in that step the problem is verified
    }
    else {
        localStorage['new_obsr_image_problem'] = 'true';
        // turning on the flag hopefully it'll be removed when submitting/refreshing :-)
        fixImageBtn();
        $('#upload_img').click(function() {
            $('#id_image').click();
        });
    }
}

$(document).ready(function() {
    window.onbeforeunload = function () {
        if (!(localStorage['new_obsr_image_problem_verified'] == 'true')) {
            // remove flags when refreshing and problem isn't verified
            localStorage.removeItem('new_obsr_image_problem');
            localStorage.removeItem('new_obsr_image_msg');
        }
        return gettext('You have unsaved changes!');
    };

    checkImageUploadIssue();

    updateDateTime();


    // handling the GPS switch
    $('.gps-btn-toggle').click(function() {
        var override_in_case = true;
        /*
            in case of an error in the form, it remembers the previous gps location,
            so the user can decide to save it instead of taking a new one.
         */
        if ($('#gpsOFF').hasClass('active')
                && $('#id_gps_accuracy').val() != "-1") {
            var msg = gettext('It seems that you already have a gps point since last page refresh,');
            msg += "\n" + gettext('click "Ok" to override this point with a new one.')
            if (!confirm(msg)) {
                override_in_case = false;

                // mark the previous point on the map
                var point = L.latLng($('#id_gps_lat').val(), $('#id_gps_lon').val());
                updateGPSMarkerOnMap(point);
            }
        }

        if (override_in_case) {
            gpsSwitchReverseDisplay();

            if ($('#gpsON').hasClass('active')) {
                detectGeoLocation();
            }
            else {
                stopGeoLocation();
            }
        }

    });

});
/* to disable the keyboard on mobile */
//$('#id_obsr_date').on('focus', function() {
//   this.blur();
//});

//watchID = navigator.geolocation.watchPosition(update_long_lang, handleError, {enabaleHighAccuracy: true, maximumAge: 0});
function update_long_lang(position)
{
	document.getElementById('id_gps_lat').value = position.coords.latitude;
	document.getElementById('id_gps_lon').value = position.coords.longitude;
	document.getElementById('id_gps_accuracy').value = position.coords.accuracy;
    if ($('accuracy_label'))
	    document.getElementById('accuracy_label').innerHTML = position.coords.accuracy;

    point = L.latLng(position.coords.latitude, position.coords.longitude);
    updateGPSMarkerOnMap(point);
};

function handleError(error) {
    var msg;
    gpsSwitchReverseDisplay();
    stopGeoLocation();
    document.getElementById('id_gps_accuracy').value = -1.0;
    switch (error.code) {
        case error.PERMISSION_DENIED:
            msg = gettext("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            msg = gettext("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            msg = gettext("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            msg = gettext("An unknown error occurred.");
            break;
    }
    msg += "\n" + gettext('Please refresh');
    alert(msg);
}

var minAccuracy = 70;
function submitTurtlesForm() {
    if ($('#id_obsr_date').val() == '') {
        alert(gettext('Date field is required'));
        $('#id_obsr_date').focus();
        return false;
    }
    if ($('#id_obsr_time').val() == '') {
        alert(gettext('Time field is required'));
        $('#id_obsr_time').focus();
        return false;
    }
    if ($('#id_gps_accuracy').val() == "-1") {
        if ($('#id_point').val() == '') {
            alert(gettext('Point is missing'));
            $('#id_point').focus();
            return false;
        }
    }
    else {
        if (parseInt($('#id_gps_accuracy').val()) > minAccuracy) {
            var msg = gettext('Accuracy level is above');
            msg += " " + minAccuracy + ",\n";
            msg += gettext('You can turn on the Wi-Fi and wait 30 seconds to try and get more accurate result.');
            msg += "\n" + gettext('Save observaion anyway') + "?";
            if (!confirm(msg)) {
                return false;
            }
        }
    }
    window.onbeforeunload = null;

    if (!(localStorage['new_obsr_image_problem_verified'] == 'true')) {
        // remove flags when submit succeed and problem isn't verified
        localStorage.removeItem('new_obsr_image_problem');
        localStorage.removeItem('new_obsr_image_msg');
    }

    return true;
}

function hasHtml5Validation () {
 return typeof document.createElement('input').checkValidity === 'function';
}

$("#id_tail_length").parent().after($("#tail_collapse"))
$("#id_species").parent().after($("#species_collapse"))