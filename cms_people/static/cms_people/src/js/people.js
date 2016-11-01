var resultWrapperMargin = 20;
var resultWrapperTop = 90;

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='<a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var $resultWrapper = $('#results');
var $results = $resultWrapper.find('.panel-body');

function resize(){
    var md = new MobileDetect(window.navigator.userAgent);
    if(md.mobile()){
        $resultWrapper.height($(window).height() - resultWrapperTop);
        $resultWrapper.width($(window).width() - resultWrapperMargin * 2);
    }
}


$resultWrapper.find('.close').on('click', function () {
    // Hide results con close click
    $resultWrapper.hide();
});


$(window).resize(function(){
    resize();
});

resize();


function getResults(pks){
    $.ajax(RESULTS_URL, {
        data: {'pks': pks.join(',')},
        success: function (data) {
            $resultWrapper.show();
            $results.html(data);
        }
    });
}

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


markers.on('click', function (marker) {
    getResults([marker.layer.options.pk]);
});


markers.on('clusterclick', function (markers) {
    getResults(_.map(markers.layer.getAllChildMarkers(), function(x){ return parseInt(x.options.pk) }).sort());
});
