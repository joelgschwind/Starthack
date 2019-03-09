function myMap() {
    var mapProp= {
        center:new google.maps.LatLng(47.423137, 9.373181),
        zoom:15,
        mapTypeId: 'satellite',
        disableDefaultUI: true,
        tilt: 0,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
    var markers = [];

    var myLatLng = {lat: latitude, lng: longitude};

    google.maps.event.addListener(map, 'click', function(event) {
        if(markers.si)
        markers.push(event.latLng);
        placeMarker(event.latLng);
    });

    function placeMarker(latLng) {
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: latitude + ', ' + longitude 
        });    
    }
}