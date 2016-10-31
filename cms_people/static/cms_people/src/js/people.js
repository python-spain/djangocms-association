var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='<a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

var mymap = L.map('mapid').setView([51.505, -0.09], 8);
var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12, attribution: osmAttrib});
mymap.addLayer(osm);
