// Adds and removes classes in footer depending on screen width.
function screenClass() {
    if(window.innerWidth < 769) {
        console.log("Screen is smaller")
        $('#map-section').addClass('hidden')
        $('#contact-section').addClass('md-6')
    } else {
        //pass
    }
}

// JS for Forms
function datePicker() {
    $("#id_requested_date").datepicker({ dateFormat: 'dd/mm/yy' });
}

function formError() {
    if( $(".alert.alert-danger").length )
    {
        $(".full-form").addClass("animate__animated animate__shakeX")
    }
}

// Opens the modal on delete_reservation
function deleteModal() {
    $("#delete-reservation").on('click', function() {
        $('#confirmationModal').modal('show');
    });
}


// Call all functions 
$(document).ready(function () {

    screenClass();

    datePicker();
    
    deleteModal();

    formError();

});
