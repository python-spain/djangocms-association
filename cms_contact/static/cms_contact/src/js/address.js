// degrees to radians
function deg2rad(degrees){
    return Math.PI*degrees/180.0
}

// radians to degrees
function rad2deg(radians){
    return 180.0*radians/Math.PI
}

// Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0 ; // Major semiaxis [m]
WGS84_b = 6356752.3;  // Minor semiaxis [m]
halfSideInKm = 200;

// Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
function WGS84EarthRadius(lat){
    // http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * Math.cos(lat);
    Bn = WGS84_b*WGS84_b * Math.sin(lat);
    Ad = WGS84_a * Math.cos(lat);
    Bd = WGS84_b * Math.sin(lat);
    return Math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) );
}

// Bounding box surrounding the point at given coordinates,
// assuming local approximation of Earth surface as a sphere
// of radius given by WGS84
function boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm){
    lat = deg2rad(latitudeInDegrees);
    lon = deg2rad(longitudeInDegrees);
    halfSide = 1000*halfSideInKm;

    // Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat);
    // Radius of the parallel at given latitude
    pradius = radius*Math.cos(lat);

    latMin = lat - halfSide/radius;
    latMax = lat + halfSide/radius;
    lonMin = lon - halfSide/pradius;
    lonMax = lon + halfSide/pradius;

    // return [rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax)]
    return [rad2deg(lonMin), rad2deg(latMin), rad2deg(lonMax), rad2deg(latMax)]
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

function setMapGeoposition(lat, lon){
    bbox = boundingBox(lat, lon, halfSideInKm);
    $('#map').attr('src', 'http://www.openstreetmap.org/export/embed.html?' +
        'bbox=' + bbox.join('%2C') + '&amp;layer=cyclemap&marker=' + [lat, lon].join(','))
}

function setAddressUsignGeoposition(){
    navigator.geolocation.watchPosition(function(position) {
      setMapGeoposition(position.coords.latitude, position.coords.longitude);
    });
}

$(function () {
    if ("geolocation" in navigator) {
        /* geolocation is available */
        setAddressUsignGeoposition();
    }

    $('#id_city, #id_subregion, #id_region').on('select2:select', function (ev) {
        var $input = $(ev.target);
        var $postal_code = $('#id_custom_postal_code');
        $.post(dataType, {'name': $input.val(), 'model': $input.attr('name')}, function(data){
            if(data['coords']){
                setMapGeoposition(data['coords'][1], data['coords'][0]);
            }
            if(data['postal_code']){
                $postal_code.val(data['postal_code']);
            }
            $.each(data, function(key, value){
                if(!value){
                    return
                }
                var $select = $('#id_' + key.toLowerCase());
                $select.append('<option value="' + value.id +
                                                     '" selected="selected">' + value.name + '</option>');
            });
        });
    });
});