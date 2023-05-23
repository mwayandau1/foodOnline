let autocomplete;
function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['in',]}
        }
    );
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById("id_address").placeholder = "Start typing...";
    }
    else {
        console.log('place name =>', place.name)
    }
}
