/*jshint esversion: 6 */

/* globals $ */

// Adds and removes classes in footer depending on screen width.
function screenClass() {
    if (window.innerWidth < 769) {
        $('#map-section').addClass('hidden');
        $('#contact-section').addClass('col-md-6');
    } else {
        $('#map-section').removeClass('hidden');
        $('#contact-section').removeClass('col-md-6');
    }
}

// JS for Forms
function datePicker() {
    $("#id_requested_date").datepicker({
        dateFormat: 'dd/mm/yy'
    });
}

function formError() {
    if ($(".alert.alert-danger").length) {
        $(".full-form").addClass("animate__animated animate__shakeX");
    }
}

function checkDate() {
    $("#reservation-enquiry").one('submit', (function (e) {
        e.preventDefault();
        var $this = $(this);
        var selectedDate = $('#id_requested_date').datepicker('getDate');
        if ((selectedDate.getTime() < Date.now())) {
            alert("Selected date is in the past, please choose a date in the future.");
        } else {
            $this.submit();
        }
    }));
}

// Hide the email input on 'Update Details' page, using opacity to prevent errors once the form is submitted
function hideEmail(){
    $("#customer-details-form>li:nth-child(3)").css({"opacity": 0, "margin": "-20px"})
}


// Opens the modal on delete_reservation
function deleteModal() {
    $("#delete-reservation").on('click', function () {
        $('#confirmationModal').modal('show');
    });

    $(".close").on('click', function () {
        $('#confirmationModal').modal('hide');
    });
}

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this,
            args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

var myEfficientFn = debounce(function () {
    screenClass();
}, 250);

// Trigger efficient screen class function each time screen resizes
window.addEventListener('resize', myEfficientFn);


// Call all functions 
$(document).ready(function () {

    datePicker();

    deleteModal();

    formError();

    checkDate();

    hideEmail();
});