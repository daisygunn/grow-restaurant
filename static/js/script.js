// JS for Forms

$(document).ready(function () {
    console.log('Working')

    $("#id_requested_date").datepicker({ dateFormat: 'dd/mm/yy' });

    $("#delete-reservation").on('click', function() {
        $('#confirmationModal').modal('show');
    });

    if( $(".alert.alert-danger").length )
    {
        $(".full-form").addClass("animate__animated animate__shakeX")
    }
});
