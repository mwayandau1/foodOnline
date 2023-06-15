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


$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data_id');
        url = $(this).attr('data_url');
        data = {'food_id': food_id};
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response);
            }
        });
    });


    $('tem_qty').each(function (){
         var the_id = $(this).attr('id');
         var qty = $(this).attr('data_qty');
         $('#'+ the_id).html(qty);
    })
});
