var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='<a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

var mymap = L.map('mapid').setView(MAP_COORDS, MAP_ZOOM);
var osm = new L.TileLayer(osmUrl, {
    // minZoom: 8, maxZoom: 12,
    attribution: osmAttrib});
mymap.addLayer(osm);

markers = L.markerClusterGroup();
$.each(elements, function (key, values) {
    key = key.split(',');
    $.each(values, function () {
        markers.addLayer(L.marker(key));
    });

});
mymap.addLayer(markers);
