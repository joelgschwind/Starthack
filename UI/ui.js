var mapProp;
var map;

var startLocation;
var crosswalkLocation;
var startLocationSet = false;
var crosswalkLocationSet = false;

var directionsService;
var directionsDisplay;

function myMap() {
    mapProp= {
        center:new google.maps.LatLng(47.423137, 9.373181),
        zoom:15,
        mapTypeId: 'satellite',
        disableDefaultUI: true,
        tilt: 0,
    };
    map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

    directionsService = new google.maps.DirectionsService,
    directionsDisplay = new google.maps.DirectionsRenderer({
      map: map
    }),


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
    if (crosswalkLocationSet) {
        crosswalkLocation.setMap(null);
    }
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: lat + ' ' + lng,
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        }
    });
    crosswalkLocationSet = true;
    crosswalkLocation = marker;
}

function process() {
    getClassification(startLocation.getPosition().lat(), startLocation.getPosition().lng())
}

function setImage() {

}

var apiIP = 'http://127.0.0.1:5000/';

/**
 * Requests a classification result to a specified video.
 * Returns a "Result" object.
 */
function getClassification(lat, lng) {
    var httpRequest = new XMLHttpRequest();
    var formData = new FormData();

    formData.append('lat', lat);
    formData.append('lng', lng);
    httpRequest.open('POST', this.apiIP + 'classify');
    httpRequest.send(formData);

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            var response = httpRequest.response;
            var slice = response.indexOf('/');
            var lat = response.substring(0,slice);
            var lng = response.substring(slice + 1, response.length);
            console.log(lat + ' ' + lng);
            placeMarkerCrosswalk(parseFloat(lat), parseFloat(lng));
            document.getElementById("classificationImg").src = "../API/classification.png";
        }
    };
}
