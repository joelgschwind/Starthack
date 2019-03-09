var startLocation;
var mapProp;
var map;
var startLocationSet = false;
var resultActive = false;

function myMap() {
    mapProp= {
        center:new google.maps.LatLng(47.423137, 9.373181),
        zoom:15,
        mapTypeId: 'satellite',
        disableDefaultUI: true,
        tilt: 0,
    };
    map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng);
    });
}

function placeMarker(latLng) {
    if (startLocationSet) {
        startLocation.setMap(null);
    }
    var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        title: latLng.lat + ' ' + latLng.lng,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
        }
    });
    startLocationSet = true;
    startLocation = marker;
}

function placeMarkerCrosswalk(lat, lng) {
    console.log(lat + ' ' + lng);
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: lat + ' ' + lng,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        }
    });
}

function process() {

}

var apiIP = 'http://127.0.0.1:5000/';

/**
 * Requests a classification result to a specified video.
 * Returns a "Result" object.
 */
function getClassification(lat, lng) {
    const httpRequest = new XMLHttpRequest();
    const formData = new FormData();

    formData.append('lat', lat);
    formData.append('lng', lng);
    httpRequest.open('POST', this.apiIP + 'classify');
    httpRequest.send(formData);

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
        const response = httpRequest.response;
        const resultObj = JSON.parse(response);

        /*
        for (const i of resultObj.segments) {
            console.log(i.start);
            for (const j of i.gestures) {
            console.log(j.name);
            }
        }
        */
        }
    };
}
