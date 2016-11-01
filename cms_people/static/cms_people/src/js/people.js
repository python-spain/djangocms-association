var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='<a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

var mymap = L.map('mapid').setView(MAP_COORDS, MAP_ZOOM);
var osm = new L.TileLayer(osmUrl, {
    // minZoom: 8, maxZoom: 12,
    attribution: osmAttrib});
mymap.addLayer(osm);


L.Marker.extend({
    options: {
        pk: null
    }
});


markers = L.markerClusterGroup();
$.each(elements, function (key, values) {
    key = key.split(',');
    $.each(values, function (i, value) {
        markers.addLayer(L.marker(key, {pk: value}));
    });

});
mymap.addLayer(markers);


markers.on('click', function (a) {
    console.log(a.layer);
});


markers.on('clusterclick', function (a) {
    // a.layer is actually a cluster
    console.log(a.layer.getAllChildMarkers());
});
