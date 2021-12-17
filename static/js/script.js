// Reservation form 

$(document).ready(function() {
    console.log('Working')

    // Hide .full-form if user is not logged in
    if($('#msg.alert-danger').length){
        console.log('alert exists')
        $(".full-form").addClass('hidden')
    }
});





