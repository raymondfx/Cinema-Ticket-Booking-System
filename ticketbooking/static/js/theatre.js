var booked_seats = [];

// It displays loader
function display_loader()
{
  jQuery("#loader").show();
}

// It hides loader
function hide_loader()
{
  jQuery("#loader").hide();
}

function isEmail(emailAddress) {
  var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
  return pattern.test(emailAddress);
}

jQuery(document).on('click', '.empty', function(){
	var seat_no = jQuery(this).attr('id');
	if (booked_seats.length === 0) {
	    booked_seats.push(seat_no);
	    jQuery(this).addClass("hold").removeClass("empty");
	}
	else
	{
		if (jQuery.inArray(seat_no, booked_seats) == -1)
		{
	  		booked_seats.push(seat_no);
	  		jQuery(this).addClass("hold").removeClass("empty");
		}
	}
});

jQuery(document).on('click', '.hold', function(){
	var seat_no = jQuery(this).attr('id');

	if ((booked_seats.length != 0) && (jQuery.inArray(seat_no, booked_seats) != -1))
	{
	    removeElm(booked_seats, seat_no);
	  	jQuery(this).addClass("empty").removeClass("hold");
	}
});


function removeElm(array, element) {
    var index = array.indexOf(element);
    if (index > -1) {
       array.splice(index, 1);
    }
}

jQuery(document).on('click', '#book_now', function(){
    jQuery("#name").val("");
    jQuery("#email").val("");
    jQuery("#name_error").hide();
    jQuery("#email_error").hide();
	if (booked_seats.length === 0) {
		alert ("Please select seats first.");
		return false;
	}
	else
	{
		var msg = "You have selected seat number " + booked_seats.join(", ") + ".";
		jQuery("#bk_seat_text").text(msg);
		jQuery("#seat_no").val(booked_seats);
		jQuery("#bookingModal").modal("show");
	}
});

// It is for booking seats
jQuery(document).on('click', '#bk_submit', function(e){
    display_loader()
	e.preventDefault();
	var returnType = true;
	jQuery(".custom-hide").text("");

	var name = jQuery("#booking_form #name").val().trim();
	var email = jQuery("#booking_form #email").val().trim();

	if (name == "")
    {
        returnType = false;
        jQuery("#booking_form #name_error").text("Please enter the name.");
        jQuery("#booking_form #name_error").show();
    }
    if (email == "")
    {
        returnType = false;
        jQuery("#booking_form #email_error").text("Please enter the email.");
        jQuery("#booking_form #email_error").show();
    }
    else
    {
        if (isEmail(email) == false)
        {
            returnType = false;
            jQuery("#booking_form #email_error").text("Please enter valid email.");
        }
    }

    if (returnType)
    {
        jQuery.ajax({
            type: "POST",
            url: "/confirm_booking/",
            data: jQuery("#booking_form").serialize(),
            cache: false,
            dataType: "json",
            success: function(data){
                hide_loader()
                if (data.status)
                {
                    jQuery("#bookingModal").modal("hide");
                    jQuery("#bk_seat_nos").html(data.seats_html);
                    booked_seats = [];
                    alert(data.msg);
                }
            },
            error: function(data){
                hide_loader()
                errors = JSON.parse(data.responseText);
                alert(errors.msg);
            }
        });
    }
});

jQuery(document).on('click', '.booked', function(){
    jQuery("#cancellation_form #email").val("");
    jQuery("#cancellation_form #seat_no1").val("");

    var seat_no = jQuery(this).attr('id');

    jQuery("#seat_no1").val(seat_no);
    jQuery("#seatMsg").html("You have selected " + seat_no + ".");

    jQuery("#cancellationModal").modal("show");
});

// It is for ticket cancellation
jQuery(document).on('click', '#cn_booking', function(e){
    display_loader();
    e.preventDefault();
    jQuery(".custom-hide").text("");

    var email = jQuery("#cancellation_form #email").val().trim();
    var returnType = true;

    if (email == "")
    {
        returnType = false;
        jQuery("#cancellation_form #email_error").text("Please enter the email.");
        jQuery("#cancellation_form #email_error").show();
    }
    else
    {
        if (isEmail(email) == false)
        {
            returnType = false;
            jQuery("#cancellation_form #email_error").text("Please enter valid email.");
        }
    }

    if (returnType)
    {
        jQuery.ajax({
            type:"POST",
            url:"/booking_cancellation/",
            data: jQuery("#cancellation_form").serialize(),
            cache:false,
            dataType: "json",
            success:function(data)
            {
                hide_loader()
                if(data.status)
                {
                    jQuery("#cancellationModal").modal("hide");
                    jQuery("#bk_seat_nos").html(data.seats_html);
                    alert(data.msg);
                }
            },
            error: function(data){
                hide_loader()
                errors = JSON.parse(data.responseText);
                alert(errors.msg);
            }
        });
    }
});

jQuery(function(){
    jQuery('#bookingModal, #cancellationModal').on('hidden.bs.modal', function () {
        hide_loader();
    });
});


